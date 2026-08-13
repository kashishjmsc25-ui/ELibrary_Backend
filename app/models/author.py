from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import UUIDMixin, TimestampMixin


class Author(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "authors"

    name = Column(String, nullable=False, index=True)
    bio = Column(String, nullable=True)

    books = relationship("Book", back_populates="author")
