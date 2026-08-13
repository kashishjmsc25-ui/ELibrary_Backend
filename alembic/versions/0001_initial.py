from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='0001_initial'; down_revision=None; branch_labels=None; depends_on=None

def upgrade():
     role = sa.Enum(
        'ADMIN',
        'LIBRARIAN',
        'MEMBER',
        name='userrole'
    )

     borrow = sa.Enum(
        'BORROWED',
        'RETURNED',
        'OVERDUE',
        name='borrowstatus'
    )

     reservation = sa.Enum(
        'ACTIVE',
        'FULFILLED',
        'CANCELLED',
        'EXPIRED',
        name='reservationstatus'
    )
     op.create_table('users',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('email',sa.String(),nullable=False),sa.Column('username',sa.String(),nullable=False),sa.Column('hashed_password',sa.String(),nullable=False),sa.Column('role',role,nullable=False),sa.Column('is_active',sa.Boolean(),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False)); op.create_index('ix_users_email','users',['email'],unique=True); op.create_index('ix_users_username','users',['username'],unique=True)
     op.create_table('authors',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('name',sa.String(),nullable=False),sa.Column('bio',sa.String()),sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False)); op.create_index('ix_authors_name','authors',['name'])
     op.create_table('categories',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('name',sa.String(),nullable=False),sa.Column('description',sa.String())); op.create_index('ix_categories_name','categories',['name'],unique=True)
     op.create_table('books',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('title',sa.String(),nullable=False),sa.Column('isbn',sa.String(),nullable=False),sa.Column('description',sa.String()),sa.Column('total_copies',sa.Integer(),nullable=False),sa.Column('available_copies',sa.Integer(),nullable=False),sa.Column('page_count',sa.Integer()),sa.Column('language',sa.String()),sa.Column('published_date',sa.Date()),sa.Column('author_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('authors.id'),nullable=False),sa.Column('category_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('categories.id'),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False)); op.create_index('ix_books_title','books',['title']); op.create_index('ix_books_isbn','books',['isbn'],unique=True)
     op.create_table('reservations',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('user_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('users.id'),nullable=False),sa.Column('book_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('books.id'),nullable=False),sa.Column('reserved_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.Column('expires_at',sa.DateTime(timezone=True),nullable=False),sa.Column('status',reservation,nullable=False))
     op.create_table('borrow_records',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('user_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('users.id'),nullable=False),sa.Column('book_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('books.id'),nullable=False),sa.Column('borrowed_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.Column('due_date',sa.DateTime(timezone=True),nullable=False),sa.Column('returned_at',sa.DateTime(timezone=True)),sa.Column('status',borrow,nullable=False),sa.Column('fine_amount',sa.Float(),nullable=False))
     op.create_table('reviews',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('user_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('users.id'),nullable=False),sa.Column('book_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('books.id'),nullable=False),sa.Column('rating',sa.Integer(),nullable=False),sa.Column('comment',sa.String()),sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.UniqueConstraint('user_id','book_id',name='uq_review_user_book'))
     op.create_table('book_summaries',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('book_id',postgresql.UUID(as_uuid=True),sa.ForeignKey('books.id'),nullable=False),sa.Column('summary_text',sa.String(),nullable=False),sa.Column('model_used',sa.String(),nullable=False),sa.Column('generated_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False)); op.create_index('ix_book_summaries_book_id','book_summaries',['book_id'],unique=True)

def downgrade():
    for t in ['book_summaries','reviews','borrow_records','reservations','books','categories','authors','users']: op.drop_table(t)
    for n in ['reservationstatus','borrowstatus','userrole']:
        sa.Enum(name=n).drop(op.get_bind(),checkfirst=True)
