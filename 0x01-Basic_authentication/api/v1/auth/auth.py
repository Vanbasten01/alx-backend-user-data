#!/usr/bin/env python3
""" auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class representing authentication functionality."""
    def __init__(self):
        """Initialize the Auth class."""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if authentication is required for the given path,
         considering excluded paths."""
        if path is None:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        path_slash = path if path.endswith("/") else path + "/"
        for exc_path in excluded_paths:
            exc_slash = exc_path if exc_path.endswith("/") else exc_path + "/"
            if path_slash.startswith(exc_slash):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user based on the request."""
        return None
