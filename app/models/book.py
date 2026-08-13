from sqlalchemy import Column,String,Integer,Date,ForeignKey,CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import UUIDMixin,TimestampMixin
class Book(Base,UUIDMixin,TimestampMixin):
    __tablename__='books'
    __table_args__=(CheckConstraint('total_copies >= 0'),CheckConstraint('available_copies >= 0'),CheckConstraint('available_copies <= total_copies'))
    title=Column(String,nullable=False,index=True); isbn=Column(String,unique=True,nullable=False,index=True); description=Column(String,nullable=True)
    total_copies=Column(Integer,nullable=False,default=1); available_copies=Column(Integer,nullable=False,default=1); page_count=Column(Integer,nullable=True); language=Column(String,nullable=True); published_date=Column(Date,nullable=True)
    author_id=Column(UUID(as_uuid=True),ForeignKey('authors.id'),nullable=False); category_id=Column(UUID(as_uuid=True),ForeignKey('categories.id'),nullable=False)
    author=relationship('Author',back_populates='books'); category=relationship('Category',back_populates='books'); reservations=relationship('Reservation',back_populates='book',cascade='all, delete-orphan'); borrow_records=relationship('BorrowRecord',back_populates='book'); reviews=relationship('Review',back_populates='book',cascade='all, delete-orphan'); summary=relationship('BookSummary',back_populates='book',uselist=False,cascade='all, delete-orphan')
