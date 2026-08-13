from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.base import UUIDMixin


class Category(Base, UUIDMixin):
    __tablename__ = "categories"

    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)

    books = relationship("Book", back_populates="category")
