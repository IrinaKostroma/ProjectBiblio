from sqlalchemy.orm import registry

from book.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.Book, tables.books)

mapper.map_imperatively(dataclasses.BookUser, tables.books_users)
