import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.models.book import Book
from app.models.book_summary import BookSummary


def get_cached(db, book_id):
    return db.query(BookSummary).filter(
        BookSummary.book_id == book_id
    ).first()


def generate(db, book_id, force=False):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(404, "Book not found")

    if not force:
        cached = get_cached(db, book_id)
        if cached:
            return cached, True

    if not settings.AI_API_KEY:
        raise HTTPException(
            503,
            "AI summary is not configured. Set AI_API_KEY."
        )

    prompt = (
        f"Create a concise, factual 2-4 paragraph summary for an "
        f"e-library. Do not invent facts.\n"
        f"Title: {book.title}\n"
        f"ISBN: {book.isbn}\n"
        f"Description: {book.description or 'Not provided'}\n"
        f"Author: {book.author.name}\n"
        f"Category: {book.category.name}\n"
        f"Language: {book.language or 'Unknown'}\n"
        f"Pages: {book.page_count or 'Unknown'}"
    )

    url = settings.AI_API_BASE_URL.rstrip("/") + "/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
    }

    try:
        r = httpx.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        r.raise_for_status()
        data = r.json()

    except httpx.HTTPError as exc:
        raise HTTPException(
            502,
            f"AI provider request failed: {exc}"
        )

    text = None

    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        text = None

    if not text:
        raise HTTPException(
            502,
            "AI provider returned no summary text"
        )

    summary = get_cached(db, book_id)

    if summary:
        summary.summary_text = text.strip()
        summary.model_used = settings.AI_MODEL
    else:
        summary = BookSummary(
            book_id=book_id,
            summary_text=text.strip(),
            model_used=settings.AI_MODEL
        )
        db.add(summary)

    db.commit()
    db.refresh(summary)

    return summary, False
