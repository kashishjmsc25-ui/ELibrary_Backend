import os
os.environ.setdefault('DATABASE_URL','sqlite:///./test.db')
os.environ.setdefault('SECRET_KEY','test-secret')
from fastapi.testclient import TestClient
from app.main import app

def test_root():
    r=TestClient(app).get('/'); assert r.status_code==200; assert r.json()['name']=='E-Library Management System API'
def test_health():
    r=TestClient(app).get('/health'); assert r.status_code==200
