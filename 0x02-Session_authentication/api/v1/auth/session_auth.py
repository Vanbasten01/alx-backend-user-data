#!/usr/bin/env python3
""" session_auth module """


from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """SessionAuth class for handling session-based authentication."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session ID for the given user ID and store it."""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
