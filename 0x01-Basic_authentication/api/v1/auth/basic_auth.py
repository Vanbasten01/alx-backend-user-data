#!/usr/bin/env python3
"""basic_auth module """
from api.v1.auth.auth import Auth


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
