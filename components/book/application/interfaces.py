from abc import ABC, abstractmethod
from typing import Optional, List

from .dataclasses import Book, BookUser


class BooksRepo(ABC):

    @abstractmethod
    def get_by_id(self, isbn13: int) -> Optional[Book]: ...

    @abstractmethod
    def get_all_id(self): ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def get_rows(self) -> int: ...

    @abstractmethod
    def add(self, book: Book): ...

    @abstractmethod
    def get_or_create(self, id_: Optional[int]) -> Book: ...

    @abstractmethod
    def remove(self, book: Book) -> None: ...

    @abstractmethod
    def exists(self, isbn13: int) -> bool: ...

    @abstractmethod
    def big_search(self, filters=None, key=None,
                   min_price=None, max_price=None,
                   order_by_price=None, order_by_size=None) -> List[Book]: ...

    @abstractmethod
    def add_all(self, books): ...

    @abstractmethod
    def get_top_n(self, top_n: int, offset: int): ...


class BooksUsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[BookUser]: ...

    @abstractmethod
    def get_by_isbn(self, isbn13: int) -> Optional[BookUser]: ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[BookUser]: ...

    @abstractmethod
    def add(self, book_user: BookUser) -> BookUser: ...

    @abstractmethod
    def get_all(self) -> Optional[BookUser]: ...
