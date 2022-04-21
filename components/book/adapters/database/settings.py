import os

from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_URL: str = f"postgresql+psycopg2://" \
                      f'{os.getenv("DB_USER", "user")}:' \
                      f'{os.getenv("DB_PASSWORD", "password")}@' \
                      f'{os.getenv("DB_HOST", "localhost")}:' \
                      f'{os.getenv("DB_PORT", "5432")}/' \
                      f'{os.getenv("DB_DATABASE", "books_database")}'

    # DB_URL: str = 'sqlite:///C:\\temp\\project.db'
