from datetime import datetime
from typing import Optional

import attr


@attr.dataclass
class Book:
    error: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    authors: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    isbn10: Optional[str] = None
    isbn13: Optional[int] = None
    pages: Optional[int] = None
    year: Optional[int] = None
    rating: Optional[int] = None
    desc: Optional[str] = None
    price: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    end_booking: Optional[str] = None
    buy_user_id: Optional[int] = None


@attr.dataclass
class BookUser:
    isbn13: Optional[int] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    user_id: Optional[int] = None
    end_booking: Optional[str] = None
    buy_user_id: Optional[int] = None
    id: Optional[int] = None
