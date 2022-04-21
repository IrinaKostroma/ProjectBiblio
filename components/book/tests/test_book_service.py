from attr import asdict

from book.application.services import BookInfoForChange

data = {
    'title': 'title1',
    'author': 'author1',
    'user_id': None,
    'id': 1,
}

def test_add_book(service, books_repo):
    service.add_book(data)
    service.books_repo.add.assert_called_once()


def test_get_book(service, books_repo):
    data = {
        'id': 1,
    }
    assert service.get_book(**data) == books_repo.get_by_id()


def test_get_all_books(service, books_repo):
    assert service.get_all_books() == books_repo.get_all()


def test_remove_book(service, books_repo):
    service.remove_book(id=1)
    service.books_repo.remove.assert_called_once()
