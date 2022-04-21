from kombu import Connection
from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext

from book.adapters import database, message_bus
from book.application import services


class Settings:
    db = database.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    books_repo = database.repositories.BooksRepo(context=context)
    books_users_repo = database.repositories.BooksUsersRepo(context=context)


class Application:
    books = services.BookService(
        books_repo=DB.books_repo,
        books_users_repo=DB.books_users_repo,
        publisher=None,
    )


class MessageBusConsumer:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.books)


    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme_cons.declare(MessageBusConsumer.connection)


if __name__ == '__main__':
    MessageBusConsumer.declare_scheme()
    MessageBusConsumer.consumer.run()
