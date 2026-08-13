from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user,require_admin
from app.models.author import Author
from app.models.category import Category
from app.schemas import AuthorCreate,AuthorOut,CategoryCreate,CategoryOut
router=APIRouter()
@router.get('/authors',response_model=list[AuthorOut])
def authors(db:Session=Depends(get_db)): return db.query(Author).order_by(Author.name).all()
@router.post('/authors',response_model=AuthorOut,status_code=201)
def add_author(data:AuthorCreate,db:Session=Depends(get_db),_=Depends(require_admin)): 
    a=Author(**data.model_dump()); db.add(a); db.commit(); db.refresh(a); return a
@router.get('/categories',response_model=list[CategoryOut])
def categories(db:Session=Depends(get_db)): return db.query(Category).order_by(Category.name).all()
@router.post('/categories',response_model=CategoryOut,status_code=201)
def add_category(data:CategoryCreate,db:Session=Depends(get_db),_=Depends(require_admin)):
    c=Category(**data.model_dump()); db.add(c); db.commit(); db.refresh(c); return c
