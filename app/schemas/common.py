from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.user import UserRole
from app.models.borrow_record import BorrowStatus
from app.models.reservation import ReservationStatus

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserOut(ORMModel):
    id: UUID; email: str; username: str; role: UserRole; is_active: bool; created_at: datetime

class RegisterRequest(BaseModel):
    email: str; username: str = Field(min_length=3,max_length=80); password: str = Field(min_length=8,max_length=128)
    @field_validator("email")
    @classmethod
    def normalize_email(cls,v): return v.strip().lower()

class LoginRequest(BaseModel):
    email: str; password: str
    @field_validator("email")
    @classmethod
    def normalize_email(cls,v): return v.strip().lower()

class TokenOut(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserOut

class AuthorCreate(BaseModel): name: str = Field(min_length=2,max_length=160); bio: str|None=None
class AuthorOut(ORMModel): id: UUID; name: str; bio: str|None; created_at: datetime
class CategoryCreate(BaseModel): name: str = Field(min_length=2,max_length=120); description: str|None=None
class CategoryOut(ORMModel): id: UUID; name: str; description: str|None

class BookCreate(BaseModel):
    title: str = Field(min_length=1,max_length=300); isbn: str = Field(min_length=10,max_length=20); description: str|None=None
    total_copies: int = Field(default=1,ge=1); page_count: int|None=Field(default=None,gt=0); language: str="English"
    published_date: date|None=None; author_id: UUID; category_id: UUID
class BookUpdate(BaseModel):
    title: str|None=None; isbn: str|None=None; description: str|None=None; total_copies: int|None=Field(default=None,ge=1)
    page_count: int|None=Field(default=None,gt=0); language: str|None=None; published_date: date|None=None; author_id: UUID|None=None; category_id: UUID|None=None
class BookOut(ORMModel):
    id: UUID; title: str; isbn: str; description: str|None; total_copies: int; available_copies: int; page_count: int|None; language: str|None; published_date: date|None; author_id: UUID; category_id: UUID; created_at: datetime
class BookDetail(BookOut):
    author_name: str; category_name: str; average_rating: float|None=None; review_count: int=0

class BorrowOut(ORMModel):
    id: UUID; user_id: UUID; book_id: UUID; borrowed_at: datetime; due_date: datetime; returned_at: datetime|None; status: BorrowStatus; fine_amount: float
class ReservationOut(ORMModel):
    id: UUID; user_id: UUID; book_id: UUID; reserved_at: datetime; expires_at: datetime; status: ReservationStatus
class ReviewCreate(BaseModel): rating: int=Field(ge=1,le=5); comment: str|None=None
class ReviewOut(ORMModel): id: UUID; user_id: UUID; book_id: UUID; rating: int; comment: str|None; created_at: datetime
class SummaryOut(ORMModel): id: UUID; book_id: UUID; summary_text: str; model_used: str; generated_at: datetime
