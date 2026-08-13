from datetime import datetime,timedelta,timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.models.book import Book
from app.models.reservation import Reservation,ReservationStatus

def expire(db):
    now=datetime.now(timezone.utc); db.query(Reservation).filter(Reservation.status==ReservationStatus.ACTIVE,Reservation.expires_at<now).update({Reservation.status:ReservationStatus.EXPIRED},synchronize_session=False); db.commit()

def create(db,user_id,book_id):
    expire(db)
    if not db.query(Book).filter(Book.id==book_id).first(): raise HTTPException(404,"Book not found")
    if db.query(Reservation).filter(Reservation.user_id==user_id,Reservation.book_id==book_id,Reservation.status==ReservationStatus.ACTIVE).first(): raise HTTPException(409,"Active reservation already exists")
    r=Reservation(user_id=user_id,book_id=book_id,expires_at=datetime.now(timezone.utc)+timedelta(hours=settings.RESERVATION_HOLD_HOURS)); db.add(r); db.commit(); db.refresh(r); return r
