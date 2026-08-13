import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models.base import UUIDMixin


class ReservationStatus(str, enum.Enum):
    ACTIVE = "active"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Reservation(Base, UUIDMixin):
    __tablename__ = "reservations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    reserved_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.ACTIVE)

    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")
