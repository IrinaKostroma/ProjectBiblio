from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

books = Table(
    'books',
    metadata,
    Column('error', String, nullable=True),
    Column('title', String, nullable=False),
    Column('subtitle', String, nullable=False),
    Column('authors', String, nullable=False),
    Column('publisher', String, nullable=False),
    Column('language', String, nullable=False),
    Column('isbn10', String, nullable=False),
    Column('isbn13', BigInteger, primary_key=True),
    Column('pages', Integer, nullable=False),
    Column('year', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('desc', Text, nullable=False),
    Column('price', String, nullable=False),
    Column('image', String, nullable=False),
    Column('url', String, nullable=False),
    Column('user_id', Integer, nullable=True),
    Column('end_booking', String, nullable=True),
    Column('buy_user_id', Integer, nullable=True),
)

books_users = Table(
    'books_users',
    metadata,
    Column('isbn13', BigInteger, nullable=False),
    Column('title', String, nullable=False),
    Column('authors', String, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('end_booking', String, nullable=True),
    Column('buy_user_id', Integer, nullable=True),
    Column('id', Integer, primary_key=True, autoincrement=True),
)
