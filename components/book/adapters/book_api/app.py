from typing import Tuple, Union

from classic.http_api import App
from classic.http_auth import Authenticator

from book.adapters.book_api import controllers, auth
from book.application import services


def create_app(books: services.BookService,
               is_dev_mode: bool,
               allow_origins: Union[str, Tuple[str, ...]],
               ) -> App:
    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(controllers.Books(authenticator=authenticator, books=books))

    return app
