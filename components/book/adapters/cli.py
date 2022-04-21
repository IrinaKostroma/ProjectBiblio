import click

from classic.messaging import Message


def create_cli(import_books_run, MessageBus, publisher):

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

        result = import_books_run(data)

        if publisher:
            publisher.plan(
                Message('user', {'action': 'send_email',
                                 'data': result
                                 }))

    return cli
