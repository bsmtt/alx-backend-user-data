#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """ Creates password hash
        Args:
            - password: user password
        Return:
            - hashed password
    """
    pwd = password.encode()
    return bcrypt.hashpw(pwd, bcrypt.gensalt())