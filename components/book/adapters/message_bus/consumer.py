from kombu import Connection

from classic.messaging_kombu import KombuConsumer

from book.application import services
from .scheme import broker_scheme_cons


def create_consumer(
    connection: Connection, books: services.BookService
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme_cons)

    consumer.register_function(
        books.import_books,
        'book',
    )

    return consumer
