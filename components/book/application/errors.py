from classic.app.errors import AppError


class NoBook(AppError):
    msg_template = "No book with ID '{number}'"
    code = 'no_book'


class BadParam(AppError):
    msg_template = "Bad param '{param}'"
    code = 'bad_param'


class BookPurchased(AppError):
    msg_template = "Book is already purchased by user with ID '{number}"
    code = 'book_purchased'


class BookTaken(AppError):
    msg_template = "Book is already taken by user with ID '{number}"
    code = 'book_taken'


class BookNoTaken(AppError):
    msg_template = "Book must be taken first"
    code = 'book_no_taken'


class OutOfTime(AppError):
    msg_template = "Booking time has expired. Take book again."
    code = 'out_of_time'


class BookNotFound(AppError):
    msg_template = "Book not found. Please try again"
    code = 'book_not_found'


class BadArgs(AppError):
    msg_template = "Bad arguments. Please try again"
    code = 'bad_args'


class EmptySearch(AppError):
    msg_template = "Empty search, try search with other keys"
    code = 'empty_search'


class BookAlreadyInDB(AppError):
    msg_template = "Book already in db, try import with new keys"
    code = 'book_already_in_db'


class NoUser(AppError):
    msg_template = "No user with ID '{number}'"
    code = 'no_user'