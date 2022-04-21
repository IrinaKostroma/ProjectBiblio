from typing import Tuple, Union

from classic.http_api import App
from classic.http_auth import Authenticator

from user.application import services
from user.adapters.user_api import controllers, auth
# from . import auth, controllers


def create_app(users: services.UserService,
               is_dev_mode: bool,
               allow_origins: Union[str, Tuple[str, ...]],
               ) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)
    authenticator.set_strategies(auth.jwt_strategy)

    app = App(prefix='/api')

    app.register(controllers.Users(authenticator=authenticator, users=users))

    return app
