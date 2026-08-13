from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user,require_admin
from app.models.reservation import Reservation,ReservationStatus
from app.schemas import ReservationOut
from app.services.reservations import create,expire
router=APIRouter()
@router.post('/{book_id}',response_model=ReservationOut,status_code=201)
def reserve(book_id,user=Depends(get_current_user),db:Session=Depends(get_db)): return create(db,user.id,book_id)
@router.get('/my',response_model=list[ReservationOut])
def my(user=Depends(get_current_user),db:Session=Depends(get_db)): expire(db); return db.query(Reservation).filter(Reservation.user_id==user.id).order_by(Reservation.reserved_at.desc()).all()
@router.delete('/{reservation_id}',response_model=ReservationOut)
def cancel(reservation_id,user=Depends(get_current_user),db:Session=Depends(get_db)):
    expire(db); r=db.query(Reservation).filter(Reservation.id==reservation_id).first()
    if not r or r.status!=ReservationStatus.ACTIVE: raise HTTPException(404,'Active reservation not found')
    if r.user_id!=user.id and user.role.value!='admin': raise HTTPException(403,'Not your reservation')
    r.status=ReservationStatus.CANCELLED; db.commit(); db.refresh(r); return r
@router.get('',response_model=list[ReservationOut])
def all_reservations(_:object=Depends(require_admin),db:Session=Depends(get_db)): expire(db); return db.query(Reservation).order_by(Reservation.reserved_at.desc()).all()
