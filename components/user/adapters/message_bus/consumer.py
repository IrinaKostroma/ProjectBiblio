from classic.messaging_kombu import KombuConsumer
from kombu import Connection

from user.application import services

from .scheme import broker_scheme_cons


def create_consumer(
    connection: Connection, users: services.UserService
) -> KombuConsumer:

    consumer = KombuConsumer(connection=connection, scheme=broker_scheme_cons)

    consumer.register_function(
        users.processing_request,
        'user',
    )

    return consumer
