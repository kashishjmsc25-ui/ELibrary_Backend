from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import require_admin
from app.models.user import User
from app.models.book import Book
from app.models.borrow_record import BorrowRecord, BorrowStatus
from app.models.reservation import Reservation, ReservationStatus
from app.models.review import Review


router = APIRouter()


@router.get("/dashboard", dependencies=[Depends(require_admin)])
def dashboard(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)

    total_books = db.query(func.count(Book.id)).scalar() or 0

    total_users = db.query(func.count(User.id)).scalar() or 0

    active_borrowings = (
        db.query(func.count(BorrowRecord.id))
        .filter(BorrowRecord.status == BorrowStatus.BORROWED)
        .scalar()
        or 0
    )

    overdue_borrowings = (
        db.query(func.count(BorrowRecord.id))
        .filter(
            BorrowRecord.status == BorrowStatus.BORROWED,
            BorrowRecord.due_date < now,
        )
        .scalar()
        or 0
    )

    active_reservations = (
        db.query(func.count(Reservation.id))
        .filter(Reservation.status == ReservationStatus.ACTIVE)
        .scalar()
        or 0
    )

    total_reviews = db.query(func.count(Review.id)).scalar() or 0

    most_borrowed = (
        db.query(
            Book.id,
            Book.title,
            func.count(BorrowRecord.id).label("borrow_count"),
        )
        .join(BorrowRecord, BorrowRecord.book_id == Book.id)
        .group_by(Book.id, Book.title)
        .order_by(func.count(BorrowRecord.id).desc())
        .first()
    )

    return {
        "total_books": total_books,
        "total_users": total_users,
        "active_borrowings": active_borrowings,
        "overdue_borrowings": overdue_borrowings,
        "active_reservations": active_reservations,
        "total_reviews": total_reviews,
        "most_borrowed_book": (
            {
                "id": str(most_borrowed.id),
                "title": most_borrowed.title,
                "borrow_count": most_borrowed.borrow_count,
            }
            if most_borrowed
            else None
        ),
    }
