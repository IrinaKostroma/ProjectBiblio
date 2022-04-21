from classic.components import component
from classic.http_auth import authenticator_needed, authenticate

from book.application import services

from .join_points import join_point


@component
@authenticator_needed
class Books:
    books: services.BookService

    @join_point
    @authenticate
    def on_get_all_books(self, request, response):
        books = self.books.get_all_books()
        response.media = [
            {'isbn13': book.isbn13,
             'title': book.title,
             'authors': book.authors,
             'user_id': book.user_id
             } for book in books
        ]

    @join_point
    @authenticate
    def on_get_get_by_isbn13(self, request, response):
        book = self.books.get_by_isbn13(**request.params)
        response.media = {
            'isbn13': book.isbn13,
            'title': book.title,
            'authors': book.authors,
            'user_id': book.user_id,
            'end_booking': book.end_booking,
            'buy_user_id': book.buy_user_id,
        }

    @join_point
    @authenticate
    def on_get_search(self, request, response):
        books = self.books.search_books(request.params)
        response.media = [
            {
                'isbn13': book.isbn13,
                'title': book.title,
                'authors': book.authors,
                'publisher': book.publisher,
                'price': book.price,
            } for book in books
        ]

    @join_point
    @authenticate
    def on_post_import_books(self, request, response):
        self.books.import_books(**request.media)
        response.media = {
            'message': 'Book imported.'
        }

    @join_point
    @authenticate
    def on_post_take_book(self, request, response):
        book = self.books.take_book(**request.media)
        response.media = {
            'message': f'Book is taken by user with ID {1}.'
        }
        # response.media = {'isbn13': book.isbn13,
        #                   'title': book.title,
        #                   'user_id': book.user_id,
        #                   'end_booking': book.end_booking,
        #                   'buy_user_id': book.buy_user_id,
        #                   }

    @join_point
    @authenticate
    def on_post_return_book(self, request, response):
        book = self.books.return_book(**request.media)
        # response.media = {
        #     'message': f'Book ID {book.isbn13} is now ready for booking.'
        # }
        response.media = {'isbn13': book.isbn13,
                          'title': book.title,
                          'user_id': book.user_id,
                          'end_booking': book.end_booking,
                          'buy_user_id': book.buy_user_id,
                          }

    @join_point
    @authenticate
    def on_post_buy_book(self, request, response):
        book = self.books.buy_book(**request.media)

        response.media = {
            'message': f'Book is purchased by user with ID {book.user_id}.'
        }

    @join_point
    @authenticate
    def on_post_remove_book(self, request, response):
        self.books.remove_book(**request.media)
        response.media = {
            'message': 'Book removed.'
        }

    @join_point
    @authenticate
    def on_get_history(self, request, response):
        result = self.books.history()
        response.media = [
            {
                'isbn13': book.isbn13,
                'user_id': book.user_id,
                'end_booking': book.end_booking,
                'buy_user_id': book.buy_user_id,
            } for book in result
        ]
