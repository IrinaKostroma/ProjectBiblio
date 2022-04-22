from typing import List, Optional

from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import select

from book.application import interfaces
from book.application.dataclasses import Book, BookUser


@component
class BooksRepo(BaseRepository, interfaces.BooksRepo):

    def get_by_id(self, isbn13: int) -> Optional[Book]:
        query = select(Book).where(Book.isbn13 == isbn13)
        return self.session.execute(query).scalars().one_or_none()

    def get_all(self) -> List[Book]:
        query = select(Book)
        return self.session.execute(query).scalars().all()

    def get_all_id(self):
        return set([e[0] for e in self.session.query(Book.isbn13).all()])

    def add(self, book: Book):
        self.session.add(book)
        self.session.commit()
        return book

    def add_all(self, books: List[Book]):
        self.session.bulk_save_objects(books)
        self.session.flush()
        self.session.commit()

    def get_rows(self):
        return self.session.query(Book).count()

    def get_or_create(self, id_: Optional[int]) -> Book:
        if id_ is None:
            book = Book()
            self.add(book)
        else:
            book = self.get_by_id(id_)
            if book is None:
                book = Book()
                self.add(book)
        return book

    def remove(self, book: Book) -> None:
        self.session.delete(book)

    def exists(self, isbn13: int) -> bool:
        q = self.session.query(Book.isbn13)
        return self.session.query(q.exists()).scalar()  # returns True or False

    def get_top_n(self, top_n: int, offset: int):
        # query = self.session.query(Book).select_from(self.session.query(Book).offset(offset)).\
        #     order_by(Book.rating.desc()).order_by(Book.year)

        query = self.session.query(Book).offset(offset)
        last = query.cte()
        query = self.session.query(last).order_by(last.c.rating.desc()).order_by(last.c.year)

        return query.all()[0:int(top_n)]

    def big_search(self, filters=None, key=None,
                   min_price=None, max_price=None,
                   order_by_price=None, order_by_size=None) -> List[Book]:
        query = self.session.query(Book)
        if filters:
            for attr, value in filters.items():
                if value:
                    query = query.filter(getattr(Book, attr) == value)
        if key:
            query = query.where(
                Book.title.ilike(f'%{key}%')
                | Book.subtitle.ilike(f'%{key}%')
                | Book.authors.ilike(f'%{key}%')
                | Book.publisher.ilike(f'%{key}%')
                | Book.desc.ilike(f'%{key}%'))
        if min_price:
            query = query.filter(Book.price >= min_price)
        if max_price:
            query = query.filter(Book.price <= max_price)
        if order_by_price:
            query = query.order_by(Book.price)
        if order_by_size:
            query = query.order_by(Book.pages)

        return query.all()

@component
class BooksUsersRepo(BaseRepository, interfaces.BooksUsersRepo):

    def get_by_id(self, id_: int) -> Optional[BookUser]:
        query = select(BookUser).where(BookUser.id == id_)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_isbn(self, isbn13: int) -> Optional[BookUser]:
        query = select(BookUser).where(BookUser.isbn13 == isbn13 and BookUser.end_booking is not None).\
            order_by(BookUser.end_booking.desc())
        return self.session.execute(query).scalars().all()

    def get_by_user_id(self, user_id: int) -> Optional[BookUser]:
        query = select(BookUser).where(BookUser.user_id == user_id and BookUser.end_booking is not None).\
            order_by(BookUser.end_booking.desc())
        return self.session.execute(query).scalars().all()

    def add(self, book_user: BookUser):
        self.session.add(book_user)
        self.session.commit()
        return book_user

    def get_all(self) -> Optional[BookUser]:
        query = select(BookUser)
        return self.session.execute(query).scalars().all()
