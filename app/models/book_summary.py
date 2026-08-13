from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.base import UUIDMixin


class BookSummary(Base, UUIDMixin):
    __tablename__ = "book_summaries"

    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), unique=True, nullable=False)
    summary_text = Column(String, nullable=False)
    model_used = Column(String, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    book = relationship("Book", back_populates="summary")
