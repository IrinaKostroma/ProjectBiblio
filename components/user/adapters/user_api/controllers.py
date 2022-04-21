from classic.components import component
from classic.http_auth import authenticator_needed, authenticate

from user.application import services

from .join_points import join_point


@component
@authenticator_needed
class Users:
    users: services.UserService

    @join_point
    def on_post_registration(self, request, response):
        self.users.registration(**request.media)
        response.media = {'message': 'User is registered'}

    @join_point
    def on_post_login(self, request, response):
        token = self.users.login(**request.media)
        response.media = {
            "token": token
        }

    @join_point
    @authenticate
    def on_get_show_info(self, request, response):
        user = self.users.get_user(**request.params)
        response.media = {
            'user_id': user.id,
            'name': user.name,
        }

    @join_point
    @authenticate
    def on_get_all_users(self, request, response):
        users = self.users.get_all_users()
        response.media = [
            {
                'user_id': user.id,
                'name': user.name,
            } for user in users
        ]

    @join_point
    @authenticate
    def on_post_remove_user(self, request, response):
        self.users.remove_user(**request.media)
        response.media = {
            'message': 'User removed.'
        }

    @join_point
    @authenticate
    def on_get_active_book(self, request, response):
        book = self.users.active_book(**request.params)
        response.media = {'isbn13': book.isbn13,
                          'title': book.title,
                          'authors': book.authors,
                          'user_id': book.user_id,
                          'end_booking': book.end_booking,
                          }

    @join_point
    @authenticate
    def on_get_taken_books(self, request, response):
        books = self.users.taken_books(**request.params)
        response.media = [
            {'isbn13': book.isbn13,
             'title': book.title,
             'authors': book.authors,
             'user_id': book.user_id,
             'end_booking': book.end_booking,
             } for book in books
        ]

    @join_point
    def on_get_history(self, request, response):
        result = self.users.history()
        response.media = [
            {
                'isbn13': book.isbn13,
                'user_id': book.user_id,
                'end_booking': book.end_booking,
                'buy_user_id': book.buy_user_id,
            } for book in result
        ]
