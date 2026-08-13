from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.config import settings
from app.models.book import Book
from app.models.borrow_record import BorrowRecord, BorrowStatus

def borrow(db: Session,user_id,book_id):
    active=db.query(BorrowRecord).filter(BorrowRecord.user_id==user_id,BorrowRecord.status.in_([BorrowStatus.BORROWED,BorrowStatus.OVERDUE])).count()
    if active>=settings.BORROW_LIMIT: raise HTTPException(400,f"Borrow limit of {settings.BORROW_LIMIT} reached")
    book=db.query(Book).filter(Book.id==book_id).with_for_update().first()
    if not book: raise HTTPException(404,"Book not found")
    if book.available_copies<1: raise HTTPException(409,"No copies available; reserve the book instead")
    if db.query(BorrowRecord).filter(BorrowRecord.user_id==user_id,BorrowRecord.book_id==book_id,BorrowRecord.status.in_([BorrowStatus.BORROWED,BorrowStatus.OVERDUE])).first(): raise HTTPException(409,"You already have this book")
    now=datetime.now(timezone.utc); record=BorrowRecord(user_id=user_id,book_id=book_id,due_date=now+timedelta(days=settings.BORROW_DAYS)); book.available_copies-=1; db.add(record); db.commit(); db.refresh(record); return record

def mark_overdue(db):
    now=datetime.now(timezone.utc)
    db.query(BorrowRecord).filter(BorrowRecord.status==BorrowStatus.BORROWED,BorrowRecord.due_date<now).update({BorrowRecord.status:BorrowStatus.OVERDUE},synchronize_session=False); db.commit()

def return_book(db,user_id,borrow_id,is_admin=False):
    record=db.query(BorrowRecord).filter(BorrowRecord.id==borrow_id).with_for_update().first()
    if not record: raise HTTPException(404,"Borrow record not found")
    if not is_admin and record.user_id!=user_id: raise HTTPException(403,"You can only return your own book")
    if record.status==BorrowStatus.RETURNED: raise HTTPException(409,"Already returned")
    now=datetime.now(timezone.utc); late=max(0,(now-record.due_date).total_seconds()); days=(int(late)//86400)+(1 if int(late)%86400 else 0)
    record.returned_at=now; record.status=BorrowStatus.RETURNED; record.fine_amount=days*settings.FINE_PER_DAY
    book=db.query(Book).filter(Book.id==record.book_id).with_for_update().first(); book.available_copies=min(book.total_copies,book.available_copies+1); db.commit(); db.refresh(record); return record
