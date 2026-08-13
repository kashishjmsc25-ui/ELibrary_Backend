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
DATABASE_URL=postgresql://postgres:123456@localhost:5432/elibrary
SECRET_KEY=elibrary-super-secret-key-2026-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=60

AI_API_KEY=sk-9f4fe53522bd45799d8d19625051d58d
AI_API_BASE_URL=https://ai-api.userfacet.com
AI_MODEL=gpt-4o-mini
```

### 3. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
elibrary
```
**Note:** My .env contains a local PostgreSQL DATABASE_URL. When running this project on another system, please update DATABASE_URL with your own PostgreSQL database credentials and database name. The rest of the environment variables can be configured according to your setup.

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

```markdown
Interactive API documentation is available through Swagger UI:

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
## API Testing Flow

The APIs can be tested directly using the Swagger UI available at `/docs`.

A simple testing flow is:

1. Register a new user or use one of the sample accounts.
2. Login to obtain a JWT access token.
3. Use the **Authorize** button in Swagger to authenticate protected endpoints.
4. Browse and search books using the catalog APIs.
5. Borrow an available book and check the borrowing details.
6. Return the borrowed book and verify the updated status.
7. Create a reservation for a book and test cancellation/expiry handling.
8. Add a review and test updating and deleting it.
9. Generate an AI summary for a book.
10. Request the same summary again to verify that the cached summary is returned.
11. Use an admin account to test admin-only operations and view the dashboard.

The Swagger documentation makes it possible to test the complete workflow without requiring a separate frontend application.

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

## Key Workflows

### Borrowing & Return

The borrowing flow checks whether a book is available and whether the user has reached the borrowing limit before creating a borrow record.

When a book is borrowed, its available copy count is reduced and a due date is assigned. On return, the record is updated with the return time and the book becomes available again.

The system also handles overdue books and calculates fines based on the configured fine rate.

### Reservations

Users can reserve books and receive a temporary reservation hold.

Active reservations have an expiry time. Expired reservations are automatically marked as expired when reservation-related APIs are accessed.

Users can also cancel their active reservations.

### AI Summary Caching

Book summaries are generated using an OpenAI-compatible API and stored in the database.

When a summary is requested, the system first checks whether a cached summary already exists. If it does, the stored summary is returned without making another AI API request.

This reduces unnecessary API calls and makes repeated summary requests faster.

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

## Design Decisions

A few implementation choices were made to keep the backend simple, modular and easy to extend:

- **Service layer:** Business logic such as borrowing, returns, reservations and AI summaries is kept in separate service modules instead of putting everything inside the API routes.
- **JWT authentication:** JWT tokens are used to authenticate users and protect private endpoints.
- **Role-based access:** Admin-only operations are protected using role-based dependencies.
- **PostgreSQL:** PostgreSQL is used as the main database because the project uses UUIDs, enum types and relational constraints.
- **Database caching:** Generated AI summaries are stored in the database so repeated requests do not need another AI API call.
- **Pagination:** Book listing supports pagination to avoid returning large datasets in a single response.
- **Alembic migrations:** Database schema changes are managed through Alembic migrations instead of manually creating tables.
- **Validation:** Pydantic schemas and database constraints are used together to validate incoming data and maintain data consistency.

## Architecture Overview

The backend follows a simple layered structure:

```text
                 Client / Swagger
                        |
                        v
                 FastAPI Routers
                        |
                        v
              Request / Response Schemas
                        |
                        v
                  Service Layer
                        |
                        v
                  SQLAlchemy ORM
                        |
                        v
                    PostgreSQL
                        |
                  Alembic Migrations


              AI Summary Service
                        |
                        v
             OpenAI-compatible API
                        |
                        v
              Book Summary Cache
```

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
