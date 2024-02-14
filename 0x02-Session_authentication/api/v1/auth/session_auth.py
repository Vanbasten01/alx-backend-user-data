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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve the user ID associated with the given session ID."""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return the currently authenticated user based on the
             provided request's session cookie."""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        from models.user import User
        return User.get(user_id)
