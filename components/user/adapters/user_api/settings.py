from typing import Union, Tuple

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    IS_DEV_MODE: bool = False
    ALLOW_ORIGINS: Union[str, Tuple[str, ...]] = Field(default_factory=tuple)


