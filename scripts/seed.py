from app.database import SessionLocal
from app.core.security import hash_password
from app.models import User,UserRole,Author,Category,Book

def main():
    db=SessionLocal()
    try:
        admin=db.query(User).filter_by(email='admin@elibrary.local').first()
        if not admin: db.add(User(email='admin@elibrary.local',username='admin',hashed_password=hash_password('Admin@123'),role=UserRole.ADMIN))
        user=db.query(User).filter_by(email='user@elibrary.local').first()
        if not user: db.add(User(email='user@elibrary.local',username='demo_user',hashed_password=hash_password('User@123'),role=UserRole.MEMBER))
        tech=db.query(Category).filter_by(name='Technology').first()
        if not tech:
            tech=Category(name='Technology',description='Technology and software'); db.add(tech)
        fiction=db.query(Category).filter_by(name='Fiction').first()
        if not fiction:
            fiction=Category(name='Fiction',description='Fiction and literature'); db.add(fiction)
        db.flush()
        martin=db.query(Author).filter_by(name='Robert C. Martin').first()
        if not martin:
            martin=Author(name='Robert C. Martin',bio='Author of Clean Code.'); db.add(martin)
        orwell=db.query(Author).filter_by(name='George Orwell').first()
        if not orwell:
            orwell=Author(name='George Orwell',bio='English novelist and essayist.'); db.add(orwell)
        db.flush()
        if not db.query(Book).filter_by(isbn='9780132350884').first(): db.add(Book(title='Clean Code',isbn='9780132350884',description='A practical guide to writing readable, maintainable software.',total_copies=5,available_copies=5,page_count=464,language='English',author_id=martin.id,category_id=tech.id))
        if not db.query(Book).filter_by(isbn='9780451524935').first(): db.add(Book(title='1984',isbn='9780451524935',description='A dystopian novel about surveillance, power and control.',total_copies=4,available_copies=4,page_count=328,language='English',author_id=orwell.id,category_id=fiction.id))
        db.commit(); print('Seed complete. admin@elibrary.local / Admin@123 ; user@elibrary.local / User@123')
    finally: db.close()
if __name__=='__main__': main()
