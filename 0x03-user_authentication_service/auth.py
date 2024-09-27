#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validate login

        Args:
            email (str): user email
            password (str): user password

        Returns:
            bool: user exists
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode(), user.hashed_password):
            return False
        return True


def _hash_password(password: str) -> bytes:
    """ Creates password hash
        Args:
            - password: user password
        Return:
            - hashed password
    """
    pwd = password.encode()
    return bcrypt.hashpw(pwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates unique id

    Returns:
        str: uuid
    """
    UUID = uuid4()
    return str(UUID)
