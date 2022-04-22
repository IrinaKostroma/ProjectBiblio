import hashlib
import os
from datetime import datetime
from typing import List, Optional

import jwt
import pytz
from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from classic.messaging import Message, Publisher
from pydantic import validate_arguments

from . import errors, interfaces
from .dataclasses import BookUser, User

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    name: str = None
    login: str = None
    password: str = None


class BookUserInfo(DTO):
    isbn13: Optional[int] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    user_id: Optional[int] = None
    end_booking: Optional[str] = None
    buy_user_id: Optional[int] = None
    id: Optional[int] = None


@component
class UserService:
    users_repo: interfaces.UsersRepo
    books_users_repo: interfaces.BooksUsersRepo
    publisher: Publisher

    @join_point
    @validate_with_dto
    def registration(self, user_info: UserInfo) -> Optional[User]:
        user = self.users_repo.get_by_login(user_info.login)

        if user:
            raise errors.UserExists(login=user_info.login)

        user_info.password = hashlib.sha256(bytes(user_info.password, encoding='utf-8')).hexdigest()
        user = self.users_repo.add(user_info.create_obj(User))

        return user

    @join_point
    @validate_with_dto
    def login(self, user_info: UserInfo) -> str:
        user = self.users_repo.get_by_login(user_info.login)
        if not user:
            raise errors.UserNoExists(login=user_info.login)

        user_info.password = hashlib.sha256(bytes(user_info.password, encoding='utf-8')).hexdigest()
        if user.password != user_info.password:
            raise errors.BadPassword()

        secret_key = os.getenv('SECRET_KEY')
        token = jwt.encode({'sub': user.id,
                            'login': user.login,
                            'name': user.name,
                            'group': 'User'}, secret_key, algorithm='HS256')
        return token

    @join_point
    @validate_arguments
    def get_user(self, user_id: int) -> User:
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.NoUser(number=user_id)
        return user

    @join_point
    @validate_arguments
    def get_all_users(self) -> List[User]:
        users = self.users_repo.get_all()
        return users

    @join_point
    @validate_arguments
    def remove_user(self, user_id: int):
        user = self.get_user(user_id)
        self.users_repo.remove(user)

    def processing_request(self, action: str, data):
        if action == 'send_email':
            ...

        elif action == 'take_book':
            # add info in history
            book_user_info = BookUserInfo(isbn13=data['isbn13'],
                                          title=data['title'],
                                          authors=data['authors'],
                                          user_id=data['user_id'],
                                          end_booking=data['end_booking'],
                                          buy_user_id=None)
            self.books_users_repo.add(book_user_info.create_obj(BookUser))

        elif action == 'return_book':
            # update info in history
            book_user_info = BookUserInfo(end_booking=data['end_booking'])
            book_user = self.books_users_repo.get_by_id(data['id'])
            book_user_info.populate_obj(book_user)
            self.books_users_repo.get_by_id(data['id'])

        elif action == 'buy_book':
            # add info in history
            book_user_info = BookUserInfo(isbn13=data['isbn13'],
                                          title=data['title'],
                                          authors=data['authors'],
                                          user_id=data['user_id'],
                                          end_booking=data['end_booking'],
                                          buy_user_id=None)
            self.books_users_repo.add(book_user_info.create_obj(BookUser))

    def send_email(self, id: Optional[int], name: str, password: str):
        user_info = UserInfo(name=name, password=password)
        user = user_info.create_obj(User)
        self.users_repo.add(user)

    @join_point
    def active_book(self, user_id):
        TIME_NOW = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S")

        history_by_isbn = self.books_users_repo.get_by_user_id(user_id)
        if history_by_isbn:
            last_taken = history_by_isbn[0]
            if last_taken.end_booking >= TIME_NOW:
                return last_taken

        raise errors.NoActiveBook(number=user_id)

    @join_point
    def taken_books(self, user_id):
        books = self.books_users_repo.get_by_user_id(user_id)
        return books

    @join_point
    def history(self):
        return self.books_users_repo.get_all()
