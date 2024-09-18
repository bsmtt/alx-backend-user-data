#!/usr/bin/env python3
"""
Auth class for the API
"""
from flask import Flask, request
from typing import List, TypeVar


class Auth():
    """Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_
        ""

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        return False

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_

        Returns:
            _type_: _description_
        """
        return None

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path not in excluded_paths:
            return False

        return True
