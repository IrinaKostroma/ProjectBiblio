from unittest.mock import Mock

import pytest

from components.book.application import interfaces


@pytest.fixture(scope='function')
def books_repo(book_1, book_2):
    books_repo = Mock(interfaces.BooksRepo)
    books_repo.get_by_isbn13 = Mock(return_value=[book_1])
    books_repo.buy_book = Mock(return_value=[book_2])
    books_repo.get_all_books = Mock(return_value=[book_1, book_2])

    return books_repo


@pytest.fixture(scope='function')
def books_users_repo(book_user_1, book_user_2):
    books_users_repo = Mock(interfaces.BooksUsersRepo)
    books_users_repo.get_by_id = Mock(return_value=book_user_1)
    books_users_repo.get_all = Mock(return_value=[book_user_1, book_user_2])

    return books_users_repo
