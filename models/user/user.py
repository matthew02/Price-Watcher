# -*- coding: utf-8 -*-

"""User account management."""

import uuid

from dataclasses import dataclass, field
from typing import Dict, List

import models.user.error as UserError

from models.model import Model
from common.utils import Utils


@dataclass
class User(Model):
    """Represents a user account.

    Attributes:
        email: The user's email address.
        password: The user's plaintext password.
    """

    email: str
    password: str
    _db_collection: str = field(init=False, default='users')
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        """Searches the database by email for a user account.

        Args:
            email: The user's email address.

        Returns: A User object representing the user account.

        Raises:
            NotFoundError: If no user account is available.
        """
        try:
            return cls.find_one('email', email)
        except TypeError:
            raise UserError.NotFoundError('No user account was found'
                                          ' with this email address.')

    @classmethod
    def register_user(cls, email: str, password: str) -> bool:
        """Attempts to register a new user account.

        Args:
            email: The user's email address.
            password: The user's plaintext password.

        Returns: True if the account was successfully registered.

        Raises:
            InvalidEmailError: If the email address is invalid.
            AlreadyRegisteredError: If there is already an account registered
                                    with this email address.
        """
        if not Utils.validate_email(email):
            raise UserError.InvalidEmailError('Invalid email.')

        try:
            cls.find_by_email(email)
            raise UserError.AlreadyRegisteredError('There is already a user'
                                                   ' registered with this'
                                                   'email.')
        except UserError.NotFoundError:
            User(email, Utils.hash_password(password)).save_to_db()

        return True

    @classmethod
    def validate_login(cls, email: str, password: str) -> bool:
        """Checks for a valid user account.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns: True if the account exists and the credentials match.

        Raises:
            IncorrectPasswordError: If the user's password is incorrect.
        """
        user = cls.find_by_email(email)

        if not Utils.verify_password(password, user.password):
            raise UserError.IncorrectPasswordError('Your password '
                                                   'was incorrect.')

        return True

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
