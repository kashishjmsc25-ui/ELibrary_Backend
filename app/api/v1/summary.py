from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_admin
from app.models.book_summary import BookSummary
from app.schemas import SummaryOut
from app.services.ai_summary_service import get_cached,generate
router=APIRouter()
@router.get('/{book_id}',response_model=SummaryOut)
def cached(book_id,db:Session=Depends(get_db)):
    s=get_cached(db,book_id)
    if not s: from fastapi import HTTPException; raise HTTPException(404,'No cached summary. Generate one first.')
    return s
@router.post('/{book_id}/generate',response_model=SummaryOut)
def make(book_id,db:Session=Depends(get_db),_=Depends(require_admin)):
    s,_cached=generate(db,book_id,False); return s
@router.post('/{book_id}/regenerate',response_model=SummaryOut)
def regenerate(book_id,db:Session=Depends(get_db),_=Depends(require_admin)):
    s,_cached=generate(db,book_id,True); return s
