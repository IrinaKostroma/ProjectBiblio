from classic.messaging_kombu import KombuPublisher
from classic.sql_storage import TransactionContext
from kombu import Connection
from sqlalchemy import create_engine

from book.adapters import book_api, database, message_bus
from book.adapters.database import repositories
from book.application import services


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
    message_bus.broker_scheme_publ.declare(connection)

    publisher = KombuPublisher(
        connection=connection,
        scheme=message_bus.broker_scheme_publ,
    )


class Application:
    books = services.BookService(books_repo=DB.books_repo,
                                 books_users_repo=DB.books_users_repo,
                                 publisher=MessageBus.publisher, )
    is_dev_mode = Settings.book_api.IS_DEV_MODE
    allow_origins = Settings.book_api.ALLOW_ORIGINS


class Aspects:
    services.join_points.join(DB.context)
    book_api.join_points.join(MessageBus.publisher, DB.context)


app = book_api.create_app(books=Application.books,
                          is_dev_mode=Application.is_dev_mode,
                          allow_origins=Application.allow_origins)
