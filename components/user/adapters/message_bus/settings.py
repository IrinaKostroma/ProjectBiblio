import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    BROKER_URL: str = f'amqp://' \
                      f"{os.getenv('RABBIT_USER', 'user')}:" \
                      f"{os.getenv('RABBIT_PASSWORD', 'password')}@" \
                      f"{os.getenv('RABBIT_HOST', 'localhost')}:" \
                      f"{os.getenv('RABBIT_PORT', 5672)}"
