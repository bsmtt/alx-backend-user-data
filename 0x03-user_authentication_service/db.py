#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add new user

        Args:
            email (str): user email
            hashed_password (str): user passwod

        Returns:
            User: new user
        """
        session = self._session
        try:
            user = User(email=email, hashed_password=hashed_password)
            session.add(user)
            session.commit()
        except Exception:
            session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """find user

        Raises:
            InvalidRequestError: _description_
            NoResultFound: _description_

        Returns:
            User: found user
        """
        for attr in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update db user

        Args:
            user_id (int): _description_

        Raises:
            ValueError: _description_
        """
        user = self.find_user_by(id=user_id)
        session = self._session
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise ValueError
            setattr(user, attr, val)
        session.commit()
