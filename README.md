# E-Library Management System — Backend

A backend for an E-Library Management System built with **FastAPI and PostgreSQL**.

The project covers the main library workflow — user authentication, books and catalogue management, borrowing and returns, reservations, reviews, recommendations, admin dashboard and AI-powered book summaries.

The code is split into API routes, schemas, database models and services so the project stays easy to understand and extend.

## Features

- JWT-based user authentication
- Role-based access control for Admin, Librarian and Member users
- Author and category management
- Book CRUD operations
- Book search, filtering and pagination
- Recommended books endpoint
- Borrowing and return workflow
- Borrow limits and due-date tracking
- Automatic fine calculation for overdue books
- Book reservations with expiry handling
- Reviews and ratings with one review per user per book
- AI-powered book summary generation
- Cached AI summaries to avoid repeated API calls
- Admin dashboard with library statistics
- PostgreSQL database with Alembic migrations
- Request validation and protected API operations
- Interactive Swagger/OpenAPI documentation
- Docker and Render deployment configuration

## Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **JWT**
- **Passlib + bcrypt**
- **OpenAI-compatible API**
- **Docker**
- **Render**

## Project Structure

```text
elibrary-backend/
│
├── app/
│   ├── api/
│   │   └── v1/              # API routes
│   ├── core/                # Security and configuration
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic
│
├── alembic/
│   └── versions/            # Database migrations
│
├── scripts/
│   └── seed.py              # Sample data
│
├── tests/                   # Backend tests
├── Dockerfile
├── render.yaml
├── requirements.txt
├── alembic.ini
└── README.md
```

The project is divided into separate layers:

- **`api/v1`** handles HTTP requests and API endpoints.
- **`models`** contains the SQLAlchemy database models.
- **`schemas`** handles request and response validation using Pydantic.
- **`services`** contains the main business logic.
- **`core`** contains security and application configuration.
- **`alembic`** manages database schema migrations.
- **`scripts`** contains the seed script used to add sample data.
- **`tests`** contains backend tests.

## Setup & Running Locally

### 1. Install dependencies

Create and activate a virtual environment in Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/elibrary
SECRET_KEY=YOUR_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES=60

AI_API_KEY=YOUR_AI_API_KEY
AI_API_BASE_URL=https://ai-api.userfacet.com
AI_MODEL=gpt-4o-mini
```

### 3. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
elibrary
```

### 4. Run database migrations

```powershell
python -m alembic upgrade head
```

### 5. Add sample data

```powershell
python -m scripts.seed
```

The seed script creates sample users, authors, categories and books.

### 6. Start the server

```powershell
python -m uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Sample Accounts

The seed script creates the following accounts for local/assignment testing:

```text
Admin
Email: admin@elibrary.local
Password: Admin@123

Member
Email: user@elibrary.local
Password: User@123
```

## API Overview

### Authentication

```text
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/auth/me
```

### Authors & Categories

```text
GET    /api/v1/catalog/authors
POST   /api/v1/catalog/authors

GET    /api/v1/catalog/categories
POST   /api/v1/catalog/categories
```

### Books

```text
GET    /api/v1/books
POST   /api/v1/books
GET    /api/v1/books/recommended
GET    /api/v1/books/{book_id}
PATCH  /api/v1/books/{book_id}
DELETE /api/v1/books/{book_id}
```

The book listing supports search, author/category filtering, language filtering, availability filtering and pagination.

The recommended books endpoint provides a separate way to surface books for the logged-in user.

### Borrowing

```text
POST   /api/v1/borrow/{book_id}
POST   /api/v1/borrow/{borrow_id}/return
GET    /api/v1/borrow/my
GET    /api/v1/borrow
```

The borrowing workflow handles:

- Borrowed date
- Due date
- Return date
- Borrow status
- Available copy updates
- Borrow limits
- Fine amount
- Overdue tracking

### Reservations

```text
POST   /api/v1/reservations/{book_id}
DELETE /api/v1/reservations/{reservation_id}
GET    /api/v1/reservations/my
GET    /api/v1/reservations
```

Reservations have an expiry time and active reservations are checked before creating another reservation for the same book.

### Reviews

```text
GET    /api/v1/reviews/book/{book_id}
POST   /api/v1/reviews/book/{book_id}
PATCH  /api/v1/reviews/{review_id}
DELETE /api/v1/reviews/{review_id}
```

A user can submit only one review for a particular book.

### AI Book Summary

```text
GET    /api/v1/summary/{book_id}
POST   /api/v1/summary/{book_id}/generate
POST   /api/v1/summary/{book_id}/regenerate
```

The summary feature generates a short book summary using an AI API and stores it in the database.

### Admin Dashboard

```text
GET    /api/v1/admin/dashboard
```

The admin dashboard provides a quick view of library activity, including:

- Total books
- Total users
- Active borrowings
- Overdue borrowings
- Active reservations
- Total reviews
- Most borrowed book

The dashboard endpoint is protected and intended for admin access.

## AI Book Summary

The AI summary feature uses a simple caching approach.

When a summary is requested:

```text
User requests summary
        ↓
Check book_summaries table
        ↓
Summary already exists?
      /       \
    Yes        No
     ↓          ↓
Return       Call AI API
summary          ↓
             Save summary
                 ↓
             Return summary
```

If a summary already exists in the database, it is returned without making another AI API call. This helps reduce unnecessary API usage.

The generated summary, model used and generation time are stored in the `book_summaries` table.

The AI configuration is controlled through:

```text
AI_API_KEY
AI_API_BASE_URL
AI_MODEL
```

## Recommendations

The backend also includes a recommended-books endpoint:

```text
GET /api/v1/books/recommended
```

This gives the application a separate place for recommendation logic instead of mixing it with normal book listing and CRUD operations.

## Database Design

The backend uses separate entities for:

- Users
- Books
- Authors
- Categories
- Borrow records
- Reservations
- Reviews
- Book summaries

Relationships are maintained using foreign keys and SQLAlchemy relationships.

Database constraints are also used for important book-copy rules, such as preventing available copies from becoming greater than total copies.

Alembic is used for database schema migrations.

## Validation & Edge Cases

The backend handles cases such as:

- Borrowing when no copies are available
- Borrow limits
- Returning an already returned book
- Overdue books and fine calculation
- Expired reservations
- Duplicate active reservations
- Duplicate reviews
- Invalid ratings
- Unauthorized access to protected operations
- Invalid or missing authentication tokens
- Repeated AI summary requests
- Updating total copies while books are currently borrowed

## Testing

Backend tests are included in the `tests/` directory.

Run:

```powershell
pytest
```

The API was also tested through the generated Swagger/OpenAPI documentation during development.

## Deployment

### Render

The project includes `render.yaml` for Render deployment.

Build command:

```text
pip install -r requirements.txt && python -m alembic upgrade head
```

Start command:

```text
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Required environment variables:

```text
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
AI_API_KEY
AI_API_BASE_URL
AI_MODEL
```

### Docker

Build:

```bash
docker build -t elibrary-backend .
```

Run:

```bash
docker run --env-file .env -p 8000:8000 elibrary-backend
```

## Notes

This project was built from a high-level library management requirement.

The focus was not only on basic CRUD operations, but also on the workflows that make a library backend useful in practice — borrowing and returning books, reservations, reviews, recommendations, admin reporting and AI-assisted summaries.

PostgreSQL is used for local development because the application relies on PostgreSQL-specific features such as UUIDs and enum types.
