#!/usr/bin/env python3
"""basic_auth module """
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


# T = TypeVar('User')


class BasicAuth(Auth):
    """A class representing basic authentication functionality."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts and returns the Base64 part of the
         Basic Authorization header."""
        if not authorization_header or not isinstance(authorization_header,
                                                      str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes and returns the decoded value of a Base64
        string using base64.b64decode."""
        if not base64_authorization_header or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except base64.binascii.Error as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts and returns user credentials from a decoded
            Base64 Authorization header."""
        decoded_auth_h = decoded_base64_authorization_header
        if not decoded_auth_h or not isinstance(decoded_auth_h, str):
            return (None, None)
        if ":" not in decoded_auth_h:
            return (None, None)
        user_email, user_password = decoded_auth_h.split(":", 1)
        return (user_email, user_password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return User instance based on email and password if valid."""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
        except KeyError:
            return None
        if not user or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the User instance for the current request
             based on the provided authorization credentials."""
        auth_header = self.authorization_header(request)
        extr_auth = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(extr_auth)
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(user_email, user_pwd)
