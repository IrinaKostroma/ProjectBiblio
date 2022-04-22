import pytest

from components.book.adapters.database import tables
from components.book.adapters.database.repositories import BooksRepo


@pytest.fixture(scope='function')
def fill_db(session):
    books_data = [
        {
            "error": "0",
            "title": "Getting Started with Roo",
            "subtitle": "Rapid Application Development for Java and Spring",
            "authors": "Josh Long, Steve Mayzak",
            "publisher": "O'Reilly Media",
            "language": "English",
            "isbn10": "1449307906",
            "isbn13": 9781449307905,
            "pages": 64,
            "year": 2011,
            "rating": 3,
            "desc": "Spring Roo goes a step beyond the Spring Framework by bringing true Rapid Application Development",
            "price": "$14.99",
            "image": "https://itbook.store/img/books/9781449307905.png",
            "url": "https://itbook.store/books/9781449307905",
            "user_id": None,
            "end_booking": None,
            "buy_user_id": None,
        },
        {
            "error": "0",
            "title": "Java EE 7 Essentials",
            "subtitle": "Enterprise Developer Handbook",
            "authors": "Arun Gupta",
            "publisher": "O'Reilly Media",
            "language": "English",
            "isbn10": "1449370179",
            "isbn13": 9781449370176,
            "pages": 362,
            "year": 2013,
            "rating": 4,
            "desc": "Get up to speed on the principal technologies in the Java Platfor",
            "price": "$36.93",
            "image": "https://itbook.store/img/books/9781449370176.png",
            "url": "https://itbook.store/books/9781449370176",
            "user_id": None,
            "end_booking": None,
            "buy_user_id": None,
        },
    ]

    session.execute(tables.books.insert(), books_data)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return BooksRepo(context=transaction_context)


def test__big_search(repo, fill_db):
    result = repo.big_search(filters={'publisher': "O'Reilly Media"})

    assert len(result) == 2


def test__big_search__multiple(repo, fill_db):
    result = repo.big_search(filters={'publisher': "O'Reilly Media", 'authors': "Arun Gupta"})

    assert len(result) == 1
    assert result[0].isbn13 == 9781449370176


def test__big_search__empty_result(repo, fill_db):
    result = repo.big_search(key='{')

    assert len(result) == 0


# def test__add(repo, session, book_1):
#     initial_data = session.execute(tables.books.select()).all()
#     assert len(initial_data) == 0
#
#     repo.add(book_1)
#     session.commit()
#
#     data = session.execute(tables.books.select()).all()
#     assert len(data) == 1
