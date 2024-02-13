#!/usr/bin/env python3
"""basic_auth module """
from api.v1.auth.auth import Auth
import base64


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
