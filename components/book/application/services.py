import requests
import threading
import pytz

from typing import Optional, List
from datetime import datetime, timezone, timedelta
from pydantic import validate_arguments

from classic.components import component
from classic.aspects import PointCut
from classic.app import DTO, validate_with_dto
from classic.messaging import Message, Publisher

from . import interfaces
from .dataclasses import Book, BookUser
from .errors import NoUser, NoBook, BookTaken, BookPurchased, EmptySearch, BookAlreadyInDB, BookNoTaken, OutOfTime

join_points = PointCut()
join_point = join_points.join_point


class MyThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.res = None

    def run(self):
        self.res = requests.get(self.url)


class BookInfo(DTO):
    error: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    authors: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    isbn10: Optional[str] = None
    isbn13: Optional[int] = None
    pages: Optional[int] = None
    year: Optional[int] = None
    rating: Optional[int] = None
    desc: Optional[str] = None
    price: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    end_booking: Optional[str] = None
    buy_user_id: Optional[int] = None


class BookUserInfo(DTO):
    isbn13: Optional[int] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    user_id: Optional[int] = None
    end_booking: Optional[str] = None
    buy_user_id: Optional[int] = None
    id: Optional[int] = None


@component
class BookService:
    books_repo: interfaces.BooksRepo
    books_users_repo: interfaces.BooksUsersRepo
    publisher: Publisher

    @join_point
    @validate_arguments
    def add_book(self, book_info: BookInfo) -> Book:
        if not self.books_repo.exists(book_info.isbn13):
            book = book_info.create_obj(Book)
            self.books_repo.add(book)

        # if self.publisher_user:
        #     self.publisher_user.plan(
        #         Message('user', {'id': None,
        #                          'name': book.title,
        #                          'password': book.author,
        #                          }))
        return book

    @join_point
    def get_all_books(self) -> List[Book]:
        books = self.books_repo.get_all()
        return books

    @join_point
    @validate_arguments
    def get_by_isbn13(self, isbn13: int) -> Book:

        book = self.books_repo.get_by_id(isbn13)

        if book is None:
            # Import book by isbn13
            self.import_books(data=str(isbn13))

            # Repeat Request to bd
            book = self.books_repo.get_by_id(isbn13)

        if book is None:
            raise NoBook(number=isbn13)

        return book

    @join_point
    def search_books(self, params_search) -> List[Book]:

        # parsing search args
        authors = '' if 'authors' not in params_search else params_search.get('authors')
        publisher = '' if 'publisher' not in params_search else params_search.get('publisher')
        key = '' if 'key' not in params_search else params_search.get('key')
        min_price = None if 'min' not in params_search or params_search.get('min') == "" \
            else '$' + params_search.get('min')
        max_price = None if 'max' not in params_search or params_search.get('max') == "" \
            else '$' + params_search.get('max')
        order_by_price = None if 'order_by_price' not in params_search else params_search.get('order_by_price')
        order_by_size = None if 'order_by_size' not in params_search else params_search.get('order_by_size')

        if not (authors or publisher or key or min or max):  # empty search
            return self.get_all_books()

        # search books in local db
        books = self.books_repo.big_search(filters={'authors': authors,
                                                    'publisher': publisher},
                                           key=key,
                                           min_price=min_price,
                                           max_price=max_price,
                                           order_by_price=order_by_price,
                                           order_by_size=order_by_size)

        if books:
            return books

        # if no books are found import books from api
        data = ' '.join([authors, publisher, key])
        if not data.isspace():
            self.import_books(data)
            books = self.books_repo.big_search(filters={'authors': authors,
                                                        'publisher': publisher},
                                               key=key,
                                               min_price=min_price,
                                               max_price=max_price)
            return books

    @join_point
    def import_books(self, data):

        URL_search = 'https://api.itbook.store/1.0/search/'
        URL_books = 'https://api.itbook.store/1.0/books/'
        TOP_N = 3

        offset = self.books_repo.get_rows()

        if data.isdigit():  # search by isbn13

            isbn13_exist = self.books_repo.get_by_id(int(data))
            if isbn13_exist:
                raise BookAlreadyInDB

            resp = requests.get(URL_books + f'{int(data)}')

            if not resp.ok:
                raise EmptySearch

            book_info = BookInfo(**resp.json())
            book = book_info.create_obj(Book)
            self.books_repo.add(book)

        else:  # seearch by tags

            isbn13_exist = self.books_repo.get_all_id()
            isbn13_new = set()
            tags = data.split()

            for tag in tags:
                threads_page = [MyThread(URL_search + f'{tag}/{i}') for i in range(1, 6)]
                for thread in threads_page:
                    thread.start()
                for thread in threads_page:
                    thread.join()

                for th in threads_page:
                    if th.res.ok:
                        books = th.res.json()['books']
                        isbn13_new.update([int(book['isbn13']) for book in books])

            if len(isbn13_new) == 0:
                raise EmptySearch

            isbn13_new = isbn13_new - isbn13_exist

            if len(isbn13_new) == 0:
                raise BookAlreadyInDB

            threads = [MyThread(URL_books + f'{isbn13}') for isbn13 in isbn13_new]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.books_repo.add_all([BookInfo(**t.res.json()).create_obj(Book) for t in threads])

            top_books = self.books_repo.get_top_n(top_n=TOP_N, offset=offset)

            email_body = '\n'.join(
                [f'{b.isbn13}\tTitle: {b.title}\tYear: {b.year}\tRating: {b.rating}' for b in top_books])

            if self.publisher:
                self.publisher.plan(
                    Message('user', {'action': 'send_email',
                                     'data': email_body
                                     }))

            return email_body

    @join_point
    def get_top_n(self, TOP_N, offset):
        return self.books_repo.get_top_n(top_n=TOP_N, offset=offset)

    @join_point
    @validate_arguments
    def take_book(self, isbn13: int, user_id: int) -> Book:

        DELTA_TIME = timedelta(minutes=1)
        TIME_NOW = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M")
        TIME_END = (datetime.now(pytz.timezone('Europe/Moscow')) + DELTA_TIME).strftime("%Y-%m-%d %H:%M")

        book = self.books_repo.get_by_id(isbn13)

        if book is None:
            raise NoBook(number=isbn13)

        if book.buy_user_id is not None:
            raise BookPurchased(number=isbn13)

        if book.end_booking is not None and book.end_booking > TIME_NOW:
            raise BookTaken(number=book.user_id)

        book_info = BookInfo(isbn13=isbn13,
                             user_id=user_id,
                             end_booking=TIME_END)
        book_info.populate_obj(book)

        # add info in history
        book_user_info = BookUserInfo(isbn13=book.isbn13,
                                      title=book.title,
                                      authors=book.authors,
                                      user_id=book.user_id,
                                      end_booking=book.end_booking,
                                      buy_user_id=None)

        self.books_users_repo.add(book_user_info.create_obj(BookUser))

        if self.publisher:
            self.publisher.plan(
                Message('user', {'action': 'take_book',
                                 'data': {'isbn13': book.isbn13,
                                          'title': book.title,
                                          'authors': book.authors,
                                          'user_id': book.user_id,
                                          'end_booking': book.end_booking,
                                          'buy_user_id': None}
                                 })
            )

        return book

    @join_point
    @validate_arguments
    def return_book(self, isbn13: int, user_id: int) -> Book:

        TIME_NOW = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M")

        book = self.books_repo.get_by_id(isbn13)

        if book is None:
            raise NoBook(number=isbn13)

        book_info = BookInfo(isbn13=isbn13,
                             user_id=None,
                             end_booking=None,
                             buy_user_id=None
                             )
        book_info.populate_obj(book)

        # update info in history
        history_by_isbn = self.books_users_repo.get_by_user_id(user_id)
        if history_by_isbn:
            last_taken = history_by_isbn[0]
            if last_taken.end_booking > TIME_NOW:
                book_user = self.books_users_repo.get_by_id(last_taken.id)
                book_user_info = BookUserInfo(end_booking=TIME_NOW)
                book_user_info.populate_obj(book_user)

                if self.publisher:
                    self.publisher.plan(
                        Message('user', {'action': 'return_book',
                                         'data': {'id': last_taken.id,
                                                  'end_booking': TIME_NOW}
                                         }))

        return book

    @join_point
    @validate_arguments
    def buy_book(self, isbn13: int, user_id: int) -> Book:

        TIME_NOW = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M")

        book = self.books_repo.get_by_id(isbn13)

        if book is None:
            raise NoBook(number=isbn13)

        if book.buy_user_id is not None:
            raise BookPurchased(number=book.buy_user_id)

        if book.user_id is None:
            raise BookNoTaken(number=book.user_id)

        if book.user_id != user_id:
            raise BookTaken(number=book.user_id)

        if book.end_booking < TIME_NOW:
            raise OutOfTime()

        book_info = BookInfo(isbn13=isbn13,
                             end_booking=TIME_NOW,
                             buy_user_id=user_id
                             )
        book_info.populate_obj(book)

        return book

    @join_point
    @validate_arguments
    def remove_book(self, isbn13: int):
        book = self.get_book(isbn13)
        if book:
            self.books_repo.remove(book)

    def history(self):
        return self.books_users_repo.get_all()
