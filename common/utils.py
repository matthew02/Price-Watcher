# -*- coding: utf-8 -*-

"""Common helper utilities."""

import re

from passlib.hash import pbkdf2_sha512


class Utils(object):
    """Common helper utilities."""
    @staticmethod
    def validate_email(email: str) -> bool:
        """Check if an email address is valid."""
        r = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if r.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for secure storage."""
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        """Check a plaintext password against a password hash."""
        return pbkdf2_sha512.verify(password, hash)
