from sqlalchemy import BigInteger, Column, Integer, MetaData, String, Table

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(128), nullable=False),
    Column('login', String(128), nullable=False),
    Column('password', String(256), nullable=False),
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