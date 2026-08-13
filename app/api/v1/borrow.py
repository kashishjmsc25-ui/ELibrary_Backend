from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user,require_admin
from app.models.borrow_record import BorrowRecord
from app.models.user import User
from app.schemas import BorrowOut
from app.services.borrowing import borrow,return_book,mark_overdue
router=APIRouter()
@router.post('/{book_id}',response_model=BorrowOut,status_code=201)
def create_borrow(book_id,user=Depends(get_current_user),db:Session=Depends(get_db)): return borrow(db,user.id,book_id)
@router.post('/{borrow_id}/return',response_model=BorrowOut)
def return_borrow(borrow_id,user=Depends(get_current_user),db:Session=Depends(get_db)): return return_book(db,user.id,borrow_id,user.role.value=='admin')
@router.get('/my',response_model=list[BorrowOut])
def my(user=Depends(get_current_user),db:Session=Depends(get_db)): mark_overdue(db); return db.query(BorrowRecord).filter(BorrowRecord.user_id==user.id).order_by(BorrowRecord.borrowed_at.desc()).all()
@router.get('',response_model=list[BorrowOut])
def all_records(_:User=Depends(require_admin),db:Session=Depends(get_db)): mark_overdue(db); return db.query(BorrowRecord).order_by(BorrowRecord.borrowed_at.desc()).all()
