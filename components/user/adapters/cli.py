import click
from classic.messaging import Message


def create_cli(publisher, MessageBus):

    @click.group()
    def cli():
        pass

    @cli.command()
    def consumer():
        MessageBus.declare_scheme()
        MessageBus.consumer.run()

    @cli.command()
    @click.argument('data', nargs=-1)
    def import_books(data):
        if publisher:
            publisher.plan(Message('book', {'data': data}))

    return cli
