from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.review import Review
from app.models.book import Book
from app.schemas import ReviewCreate,ReviewOut
router=APIRouter()
@router.get('/book/{book_id}',response_model=list[ReviewOut])
def list_reviews(book_id,db:Session=Depends(get_db)): return db.query(Review).filter(Review.book_id==book_id).order_by(Review.created_at.desc()).all()
@router.post('/book/{book_id}',response_model=ReviewOut,status_code=201)
def create_review(book_id,data:ReviewCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not db.query(Book).filter(Book.id==book_id).first(): raise HTTPException(404,'Book not found')
    if db.query(Review).filter(Review.user_id==user.id,Review.book_id==book_id).first(): raise HTTPException(409,'You already reviewed this book')
    r=Review(user_id=user.id,book_id=book_id,**data.model_dump()); db.add(r); db.commit(); db.refresh(r); return r
@router.patch('/{review_id}',response_model=ReviewOut)
def update_review(review_id,data:ReviewCreate,user=Depends(get_current_user),db:Session=Depends(get_db)):
    r=db.query(Review).filter(Review.id==review_id).first()
    if not r: raise HTTPException(404,'Review not found')
    if r.user_id!=user.id and user.role.value!='admin': raise HTTPException(403,'Not your review')
    for k,v in data.model_dump().items(): setattr(r,k,v)
    db.commit(); db.refresh(r); return r
@router.delete('/{review_id}',status_code=204)
def delete_review(review_id,user=Depends(get_current_user),db:Session=Depends(get_db)):
    r=db.query(Review).filter(Review.id==review_id).first()
    if not r: raise HTTPException(404,'Review not found')
    if r.user_id!=user.id and user.role.value!='admin': raise HTTPException(403,'Not your review')
    db.delete(r); db.commit()
