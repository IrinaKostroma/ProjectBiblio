from classic.app.errors import AppError


class NoUser(AppError):
    msg_template = "No user with ID '{number}'."
    code = 'no_user'


class UserExists(AppError):
    msg_template = "User with LOGIN '{login}' already exists."
    code = 'user_exists'


class UserNoExists(AppError):
    msg_template = "User with LOGIN '{login}' doesn`t exist."
    code = 'user_no_exists'


class BadPassword(AppError):
    msg_template = "Wrong password."
    code = 'bad_password'


class NoActiveBook(AppError):
    msg_template = "User with ID {number} doesn`t have an active book now."
    code = 'no_active_book'