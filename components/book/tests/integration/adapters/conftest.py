from unittest.mock import Mock

import pytest

from components.book.application import dataclasses, services


@pytest.fixture(scope='function')
def book_service():
    service = Mock(services.BookService)

    return service


@pytest.fixture(scope='function')
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


@pytest.fixture(scope='function')
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