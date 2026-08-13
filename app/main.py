from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import auth,books,catalog,borrow,reservations,reviews,summary,admin

app=FastAPI(title='E-Library Management System',description='Production-style backend for an e-library with borrowing, reservations, reviews and AI summaries.',version='1.0.0')
origins=[x.strip() for x in settings.CORS_ORIGINS.split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins if origins!=['*'] else ['*'],allow_credentials=origins!=['*'],allow_methods=['*'],allow_headers=['*'])
@app.get('/')
def root(): return {'name':'E-Library Management System API','version':'1.0.0','docs':'/docs','health':'/health'}
@app.get('/health')
def health(): return {'status':'ok'}
app.include_router(auth.router,prefix='/api/v1/auth',tags=['auth'])
app.include_router(catalog.router,prefix='/api/v1/catalog',tags=['catalog'])
app.include_router(books.router,prefix='/api/v1/books',tags=['books'])
app.include_router(borrow.router,prefix='/api/v1/borrow',tags=['borrowing'])
app.include_router(reservations.router,prefix='/api/v1/reservations',tags=['reservations'])
app.include_router(reviews.router,prefix='/api/v1/reviews',tags=['reviews'])
app.include_router(summary.router,prefix='/api/v1/summary',tags=['ai-summary'])
app.include_router(admin.router,prefix='/api/v1/admin',tags=['admin'])
