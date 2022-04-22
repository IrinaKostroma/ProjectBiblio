from typing import List, Optional

from classic.components import component
from classic.sql_storage import BaseRepository
from sqlalchemy import select

from user.application import interfaces
from user.application.dataclasses import BookUser, User


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):

    def get_by_id(self, id_: int) -> Optional[User]:
        query = select(User).where(User.id == id_)
        user = self.session.execute(query).scalars().one_or_none()
        return user

    def get_by_login(self, login: str) -> Optional[User]:
        query = select(User).where(User.login == login)
        user = self.session.execute(query).scalars().one_or_none()
        return user

    def add(self, user: User):
        self.session.add(user)
        self.session.flush()
        self.session.commit()

    def auth(self, user: User):
        query = select(User).where(User.login == user.login and User.password == user.password)
        user = self.session.execute(query).scalars().one_or_none()
        return user

    def get_all(self) -> List[User]:
        query = select(User)  # .order_by(User.id)
        users = self.session.execute(query).scalars().all()
        return users

    def get_or_create(self, id_: Optional[int]) -> User:
        if id_ is None:
            user = User()
            self.add(user)
        else:
            user = self.get_by_id(id_)
            if user is None:
                user = User()
                self.add(user)
        return user

    def remove(self, user: User) -> None:
        self.session.delete(user)


@component
class BooksUsersRepo(BaseRepository, interfaces.BooksUsersRepo):

    def get_by_id(self, id_: int) -> Optional[BookUser]:
        self.session.commit()
        query = select(BookUser).where(BookUser.id == id_)
        return self.session.execute(query).scalars().one_or_none()

    def get_by_isbn(self, isbn13: int) -> Optional[BookUser]:
        query = select(BookUser).where(BookUser.isbn13 == isbn13 and BookUser.end_booking is not None).\
            order_by(BookUser.end_booking.desc())
        return self.session.execute(query).scalars().all()

    def get_by_user_id(self, user_id: int) -> Optional[BookUser]:
        query = select(BookUser).where(BookUser.user_id == user_id and BookUser.end_booking is not None).\
            order_by(BookUser.end_booking.desc())
        return self.session.execute(query).scalars().all()

    def add(self, book_user: BookUser):
        self.session.add(book_user)
        self.session.commit()
        return book_user

    def get_all(self) -> Optional[BookUser]:
        self.session.commit()
        query = select(BookUser)
        return self.session.execute(query).scalars().all()
