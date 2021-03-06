from unittest.mock import Mock

import pytest
from classic.messaging import Publisher

from book.application import dataclasses, interfaces, services
from book.application.services import BookService


@pytest.fixture
def book_1():
    return dataclasses.Book(
        error="0",
        title="Java EE 7 Essentials",
        subtitle="Enterprise Developer Handbook",
        authors="Arun Gupta",
        publisher="O'Reilly Media",
        language="English",
        isbn10="1449370179",
        isbn13=9781449370176,
        pages=362,
        year=2013,
        rating=4,
        desc="Get up to speed on the principal technologies in the Java Platfor",
        price="$36.93",
        image="https://itbook.store/img/books/9781449370176.png",
        url="https://itbook.store/books/9781449370176",
        user_id=1,
        end_booking="2022-04-21 10:10:10",
        buy_user_id=None,
    )


@pytest.fixture
def book_2():
    return dataclasses.Book(
        error="0",
        title="Getting Started with Roo",
        subtitle="Rapid Application Development for Java and Spring",
        authors="Josh Long, Steve Mayzak",
        publisher="O'Reilly Media",
        language="English",
        isbn10="1449307906",
        isbn13=9781449307905,
        pages=64,
        year=2011,
        rating=3,
        desc="Spring Roo goes a step beyond the Spring Framework by bringing true Rapid Application Development",
        price="$14.99",
        image="https://itbook.store/img/books/9781449307905.png",
        url="https://itbook.store/books/9781449307905",
        user_id=2,
        end_booking="2022-04-21 12:10:10",
        buy_user_id=2,
    )


@pytest.fixture
def book_info():
    return services.BookInfo(
        id=1,
        title='title1',
        author='author1',
        user_id=1,
    )


@pytest.fixture(scope='function')
def books_repo(book_1):
    books_repo = Mock(interfaces.BooksRepo)
    books_repo.add_book = Mock(return_value=book_1)
    books_repo.get_book = Mock(return_value=book_1)
    books_repo.get_all_books = Mock(return_value=[book_1, ])
    books_repo.take_by_user = Mock(return_value=book_1)
    books_repo.return_book = Mock(return_value=book_1)
    books_repo.remove_book = Mock(return_value=book_1)
    return books_repo


@pytest.fixture()
def book_publisher():
    book_publisher = Mock(Publisher)
    book_publisher.plan = Mock(return_value=None)
    return book_publisher


@pytest.fixture(scope='function')
def service(books_repo, book_publisher):
    return BookService(
        books_repo=books_repo,
        publisher=book_publisher,
    )
