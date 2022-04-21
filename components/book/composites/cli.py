from book.adapters.cli import create_cli
from .import_book import import_books as import_books_run
from book.composites.consumer import MessageBusConsumer
from book.composites.book_api import MessageBus


if __name__ == '__main__':
    cli = create_cli(import_books_run, MessageBusConsumer, MessageBus.publisher)
    cli()
