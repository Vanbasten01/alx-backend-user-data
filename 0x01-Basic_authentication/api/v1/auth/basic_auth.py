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