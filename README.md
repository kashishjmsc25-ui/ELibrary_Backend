# E-Library Management System — Complete Backend

A modular **FastAPI + PostgreSQL** backend based on the supplied ER diagram. The project now includes authentication, catalog management, borrowing, returns/fines, reservations, reviews, cached AI summaries, validation, migrations, seed data, tests and Render deployment configuration.

## Features
- JWT auth: register, login, current user
- Roles: `admin`, `librarian`, `member`
- Author/category management
- Book CRUD, search, filters and pagination
- Borrow limit, due dates, overdue status and fines
- Reservations with expiry
- One review per user per book
- AI summary generation + DB cache
- Centralized FastAPI validation/error responses
- PostgreSQL + Alembic migrations
- Swagger at `/docs`
- Render + Docker deployment files

## Run locally
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```
Set `DATABASE_URL` and a strong `SECRET_KEY` in `.env`.

Create the database `elibrary`, then:
```bash
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

Seed accounts:
- Admin: `admin@elibrary.local` / `Admin@123`
- Member: `user@elibrary.local` / `User@123`

Change these before a real deployment.

## API map
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET/POST /api/v1/catalog/authors`
- `GET/POST /api/v1/catalog/categories`
- `GET/POST/PATCH/DELETE /api/v1/books`
- `GET /api/v1/books/{id}`
- `POST /api/v1/borrow/{book_id}`
- `POST /api/v1/borrow/{borrow_id}/return`
- `GET /api/v1/borrow/my`
- `GET /api/v1/borrow` (admin)
- `POST/DELETE /api/v1/reservations/{book_id or reservation_id}`
- `GET /api/v1/reservations/my`
- `GET /api/v1/reservations` (admin)
- `GET/POST/PATCH/DELETE /api/v1/reviews/...`
- `GET /api/v1/summary/{book_id}`
- `POST /api/v1/summary/{book_id}/generate` (admin)
- `POST /api/v1/summary/{book_id}/regenerate` (admin)

## AI summary design
The summary service first checks `book_summaries`. If a cached summary exists, it is returned without an AI call. Otherwise it sends book metadata/description to an OpenAI-compatible `/responses` endpoint, stores the generated summary, and returns it. This reduces repeated API cost and latency.

Set:
```env
AI_API_KEY=...
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-5-mini
```

## Deployment
### Render
1. Push this folder to GitHub.
2. Create a PostgreSQL database.
3. Create a Web Service from the repo.
4. Render can use `render.yaml`; otherwise use:
   - Build: `pip install -r requirements.txt && alembic upgrade head`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add `DATABASE_URL`, `SECRET_KEY`, `AI_API_KEY`, and other variables.

### Docker
```bash
docker build -t elibrary-backend .
docker run --env-file .env -p 8000:8000 elibrary-backend
```

## Project structure
```text
app/
  api/v1/       # HTTP routes
  core/         # security
  models/       # SQLAlchemy entities
  schemas/      # Pydantic request/response models
  services/     # business logic
scripts/        # seed data
alembic/        # migrations
tests/          # smoke tests
```
