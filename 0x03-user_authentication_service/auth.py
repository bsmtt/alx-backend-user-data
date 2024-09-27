#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


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

    def create_session(self, email: str) -> str:
        """Returns user session ID

        Args:
            email (str): user email

        Returns:
            str: user session uuid
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """get user from session_id

        Args:
            session_id (str): session unique id

        Returns:
            Union[str, None]: User if found else None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys user session

        Args:
            user_id (int): user id

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """genereate reset password token

        Args:
            email (str): user emaol

        Raises:
            ValueError: value eror

        Returns:
            str: token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """reset password

        Args:
            email (str): user emaol

        Raises:
            ValueError: value eror

        Returns:
            None: none
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(
            user.id,
            hashed_password=_hash_password(password),
            reset_token=None
        )


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
