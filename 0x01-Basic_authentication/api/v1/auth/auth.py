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
        # path_slash = path if path.endswith("/") else path + "/"
        for exc_path in excluded_paths:
            if exc_path.endswith("*"):
                if path.startswith(exc_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Get the authorization header from the request."""
        if not request:
            return None
        if 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user based on the request."""
        return None
