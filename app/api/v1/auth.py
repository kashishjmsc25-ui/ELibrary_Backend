from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.schemas import RegisterRequest,LoginRequest,TokenOut,UserOut
from app.services.auth import register,login
router=APIRouter()
@router.post('/register',response_model=UserOut,status_code=201)
def register_user(data:RegisterRequest,db:Session=Depends(get_db)): return register(db,data.email,data.username,data.password)
@router.post('/login',response_model=TokenOut)
def login_user(data:LoginRequest,db:Session=Depends(get_db)):
    token,user=login(db,data.email,data.password); return {'access_token':token,'token_type':'bearer','user':user}
@router.get('/me',response_model=UserOut)
def me(user=Depends(get_current_user)): return user
