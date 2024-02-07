#!/usr/bin/env python3
"""Provides functions for hashing and validating passwords using bcrypt."""
from bcrypt import hashpw, gensalt, checkpw


def hash_password(password) -> bytes:
    """Hashes the password using bcrypt."""
    # generate salt using bcrypt
    salt = gensalt()
    # Hash the password using the generated salt
    hashed_pwd = hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return checkpw(password.encode('utf-8'), hashed_password)
