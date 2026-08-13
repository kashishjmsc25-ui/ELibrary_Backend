from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import or_,func
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_admin, get_current_user
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from app.models.review import Review
from app.models.borrow_record import BorrowRecord
from app.schemas import BookCreate,BookUpdate,BookOut,BookDetail
router=APIRouter()
@router.get('',response_model=dict)
def list_books(search:str|None=None,author_id=None,category_id=None,language:str|None=None,available:bool=False,page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=50),db:Session=Depends(get_db)):
    q=db.query(Book)
    if search: q=q.join(Author).filter(or_(Book.title.ilike(f'%{search}%'),Book.isbn.ilike(f'%{search}%'),Author.name.ilike(f'%{search}%')))
    if author_id: q=q.filter(Book.author_id==author_id)
    if category_id: q=q.filter(Book.category_id==category_id)
    if language: q=q.filter(Book.language.ilike(language))
    if available: q=q.filter(Book.available_copies>0)
    total=q.count(); items=q.order_by(Book.created_at.desc()).offset((page-1)*limit).limit(limit).all()
    books = [BookOut.model_validate(book).model_dump() for book in items]
    return {'data': books, 'pagination': {'page': page, 'limit': limit, 'total': total, 'pages': (total + limit - 1) // limit}}
@router.get('/recommended', response_model=list[BookOut])
def recommended_books(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find categories the user has interacted with
    borrowed_categories = (
        db.query(Book.category_id)
        .join(BorrowRecord, BorrowRecord.book_id == Book.id)
        .filter(BorrowRecord.user_id == user.id)
        .distinct()
        .all()
    )

    reviewed_categories = (
        db.query(Book.category_id)
        .join(Review, Review.book_id == Book.id)
        .filter(Review.user_id == user.id)
        .distinct()
        .all()
    )

    preferred_categories = {
        category_id
        for category_id, in borrowed_categories + reviewed_categories
    }

    # Books currently borrowed by the user
    borrowed_book_ids = (
        db.query(BorrowRecord.book_id)
        .filter(
            BorrowRecord.user_id == user.id,
            BorrowRecord.returned_at.is_(None)
        )
        .subquery()
    )

    # Available books with average rating
    books_query = (
        db.query(
            Book,
            func.coalesce(func.avg(Review.rating), 0).label("average_rating")
        )
        .outerjoin(Review, Review.book_id == Book.id)
        .filter(
            Book.available_copies > 0,
            ~Book.id.in_(borrowed_book_ids)
        )
        .group_by(Book.id)
    )

    books = books_query.all()

    # Prioritize books from categories the user has interacted with
    books.sort(
        key=lambda row: (
            row[0].category_id in preferred_categories,
            float(row[1])
        ),
        reverse=True
    )

    return [
        BookOut.model_validate(book).model_dump()
        for book, _ in books[:10]
    ]
@router.get('/{book_id}',response_model=BookDetail)
def get_book(book_id,db:Session=Depends(get_db)):
    row=db.query(Book,Author.name.label('author_name'),Category.name.label('category_name'),func.avg(Review.rating).label('average_rating'),func.count(Review.id).label('review_count')).join(Author).join(Category).outerjoin(Review).filter(Book.id==book_id).group_by(Book.id,Author.name,Category.name).first()
    if not row: raise HTTPException(404,'Book not found')
    b,a,c,avg,count=row; return {**BookOut.model_validate(b).model_dump(),'author_name':a,'category_name':c,'average_rating':float(avg) if avg is not None else None,'review_count':count}
@router.post('',response_model=BookOut,status_code=201)
def create(data:BookCreate,db:Session=Depends(get_db),_=Depends(require_admin)):
    if not db.query(Author).filter(Author.id==data.author_id).first() or not db.query(Category).filter(Category.id==data.category_id).first(): raise HTTPException(400,'Author/category not found')
    b=Book(**data.model_dump(),available_copies=data.total_copies); db.add(b); db.commit(); db.refresh(b); return b
@router.patch('/{book_id}',response_model=BookOut)
def update(book_id,data:BookUpdate,db:Session=Depends(get_db),_=Depends(require_admin)):
    b=db.query(Book).filter(Book.id==book_id).first()
    if not b: raise HTTPException(404,'Book not found')
    borrowed=b.total_copies-b.available_copies; d=data.model_dump(exclude_unset=True)
    if 'total_copies' in d and d['total_copies']<borrowed: raise HTTPException(400,'total_copies cannot be below currently borrowed copies')
    if 'total_copies' in d: b.available_copies=d['total_copies']-borrowed
    for k,v in d.items():
        if k!='total_copies': setattr(b,k,v)
    if 'total_copies' in d: b.total_copies=d['total_copies']
    db.commit(); db.refresh(b); return b
@router.delete('/{book_id}',status_code=204)
def delete(book_id,db:Session=Depends(get_db),_=Depends(require_admin)):
    b=db.query(Book).filter(Book.id==book_id).first()
    if not b: raise HTTPException(404,'Book not found')
    db.delete(b); db.commit()
