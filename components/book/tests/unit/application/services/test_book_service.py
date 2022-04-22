import pytest

from components.book.application import errors
from components.book.application.services import BookService


@pytest.fixture(scope='function')
def service(books_repo, books_users_repo):
    return BookService(books_repo=books_repo,
                       books_users_repo=books_users_repo,
                       publisher=None)


def test__get_by_isbn13(service, books_repo):
    isbn13 = 9781449370176

    service.get_by_isbn13(isbn13=isbn13)

    call_args, _ = books_repo.get_by_id.call_args
    assert call_args == (isbn13, )


def test__buy_book(service, books_repo):

    isbn13 = 9781449307905
    user_id = 2

    service.get_by_isbn13(isbn13=isbn13)

    call_args, _ = books_repo.get_by_id.call_args
    assert call_args == (isbn13, )


def test__buy_book__no_book(service, books_repo):
    books_repo.get_by_id.return_value = None

    isbn13 = 1
    user_id = 2

    with pytest.raises(errors.NoBook):
        service.buy_book(isbn13=isbn13, user_id=user_id)


def test__history(service, books_users_repo):
    service.history()

    call_args, _ = books_users_repo.get_all.call_args
    assert call_args == ()
