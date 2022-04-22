from user.adapters.cli import create_cli
from user.composites.consumer import MessageBusConsumer
from user.composites.user_api import MessageBus

if __name__ == '__main__':
    cli = create_cli(MessageBus.publisher, MessageBusConsumer)
    cli()
