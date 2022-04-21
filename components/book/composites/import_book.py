import sys
import requests
import threading

from kombu import Connection
from sqlalchemy import create_engine

from classic.messaging import Message
from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext

from book.application.services import BookInfo, Book
from book.application import services
from book.adapters.database import repositories
from book.adapters import database, book_api, message_bus
from book.application.errors import EmptySearch, BookAlreadyInDB


class Settings:
    db = database.Settings()
    book_api = book_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = repositories.BooksRepo(context=context)
    books_users_repo = repositories.BooksUsersRepo(context=context)


class MessageBus:
    connection = Connection(Settings.message_bus.BROKER_URL)
    # message_bus.broker_scheme_publ.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme_publ,
    )

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme_cons.declare(MessageBus.connection)


class Application:
    book_service = services.BookService(books_repo=DB.books_repo,
                                        books_users_repo=DB.books_users_repo,
                                        publisher=MessageBus.publisher,)
    is_dev_mode = Settings.book_api.IS_DEV_MODE
    allow_origins = Settings.book_api.ALLOW_ORIGINS


class MyThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.res = None

    def run(self):
        self.res = requests.get(self.url)


def import_books(tags):

    URL_search = 'https://api.itbook.store/1.0/search/'
    URL_books = 'https://api.itbook.store/1.0/books/'
    TOP_N = 3

    app = book_api.create_app(books=Application.book_service,
                              is_dev_mode=Application.is_dev_mode,
                              allow_origins=Application.allow_origins)

    books_repo = DB.books_repo
    MessageBus.declare_scheme()
    publisher = MessageBus.publisher

    offset = books_repo.get_rows()

    isbn13_exist = books_repo.get_all_id()
    isbn13_new = set()

    for tag in tags:
        threads_page = [MyThread(URL_search + f'{tag}/{i}') for i in range(1, 6)]
        for thread in threads_page:
            thread.start()
        for thread in threads_page:
            thread.join()

        for th in threads_page:
            if th.res:
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

    books_repo.add_all([BookInfo(**t.res.json()).create_obj(Book) for t in threads])

    top_books = books_repo.get_top_n(top_n=TOP_N, offset=offset)

    email_body = '\n'.join(
        [f'{b.isbn13}\tTitle: {b.title}\tYear: {b.year}\tRating: {b.rating}' for b in top_books])

    if publisher:
        publisher.plan(
            Message('user', {'action': 'send_email',
                             'data': email_body
                             }))

    return email_body


if __name__ == '__main__':

    import_books(*sys.argv[1:])
