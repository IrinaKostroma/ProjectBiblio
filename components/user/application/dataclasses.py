import attr

from typing import Optional

@attr.dataclass
class User:
    id: Optional[int] = None
    name: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None


@attr.dataclass
class BookUser:
    isbn13: Optional[int] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    user_id: Optional[int] = None
    end_booking: Optional[str] = None
    buy_user_id: Optional[int] = None
    id: Optional[int] = None
