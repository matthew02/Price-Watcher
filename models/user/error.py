# -*- coding: utf-8 -*-

"""User account exception handlers."""


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class NotFoundError(UserError):
    pass


class AlreadyRegisteredError(UserError):
    pass


class InvalidEmailError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass
