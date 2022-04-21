from kombu import Connection
from sqlalchemy import create_engine

from classic.sql_storage import TransactionContext
from classic.messaging_kombu import KombuPublisher

from user.adapters import database, user_api, message_bus
from user.application import services
from user.adapters.database import repositories


class Settings:
    db = database.Settings()
    user_api = user_api.Settings()
    message_bus = message_bus.Settings()


class DB:
    engine = create_engine(Settings.db.DB_URL)
    database.metadata.create_all(engine)

    context = TransactionContext(bind=engine)

    users_repo = repositories.UsersRepo(context=context)
    books_users_repo = repositories.BooksUsersRepo(context=context)


class Application:
    user_service = services.UserService(users_repo=DB.users_repo,
                                        books_users_repo=DB.books_users_repo,
                                        publisher=None)
    is_dev_mode = Settings.user_api.IS_DEV_MODE
    allow_origins = Settings.user_api.ALLOW_ORIGINS


class MessageBusConsumer:
    connection = Connection(Settings.message_bus.BROKER_URL)
    consumer = message_bus.create_consumer(connection, Application.user_service)
    # publisher = KombuPublisher(
    #     connection=connection,
    #     scheme=message_bus.broker_scheme_publ,
    # )

    @staticmethod
    def declare_scheme():
        message_bus.broker_scheme_cons.declare(MessageBusConsumer.connection)


if __name__ == '__main__':
    MessageBusConsumer.declare_scheme()
    MessageBusConsumer.consumer.run()
