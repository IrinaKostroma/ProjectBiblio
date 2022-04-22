from abc import ABC, abstractmethod
from typing import List, Optional

from .dataclasses import BookUser, User


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]: ...

    @abstractmethod
    def add(self, user: User): ...

    @abstractmethod
    def auth(self, user: User): ...

    @abstractmethod
    def get_or_create(self, id_: Optional[int]) -> User: ...

    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def remove(self, book: User) -> None: ...


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
