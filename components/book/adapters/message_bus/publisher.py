from classic.messaging_kombu import KombuPublisher
from kombu import Connection

from book.application import services

from .scheme import broker_scheme_publ


def create_publisher(
    connection: Connection, books: services.BookService
) -> KombuPublisher:

    publisher = KombuPublisher(connection=connection, scheme=broker_scheme_publ)

    # consumer.register_function(
    #     books.import_books,
    #     'book',
    # )

    return publisher
