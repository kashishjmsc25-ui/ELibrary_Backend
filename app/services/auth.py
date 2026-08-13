from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

def register(db: Session, email: str, username: str, password: str):
    if db.query(User).filter((User.email==email)|(User.username==username)).first():
        raise HTTPException(409,"Email or username already exists")
    user=User(email=email,username=username,hashed_password=hash_password(password)); db.add(user); db.commit(); db.refresh(user); return user

def login(db: Session, email: str, password: str):
    user=db.query(User).filter(User.email==email).first()
    if not user or not user.is_active or not verify_password(password,user.hashed_password):
        raise HTTPException(401,"Invalid email or password",headers={"WWW-Authenticate":"Bearer"})
    token=create_access_token({"sub":str(user.id),"role":user.role.value})
    return token,user
