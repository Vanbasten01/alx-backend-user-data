#!/usr/bin/env python3
""" module for SessionDBAuth's class """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Subclass of SessionExpAuth implementing session
         management with database support."""
    def create_session(self, user_id=None):
        """Create a new session for the given user ID and
             store it in the database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        user_session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID associated with the given
             session ID from the database."""
        if not session_id:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        if self.session_duration <= 0:
            return user_sessions[0].user_id
        if not hasattr(user_sessions[0], 'created_at'):
            return None
        created_at = user_sessions[0].created_at
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.utcnow():
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """Destroy the session associated with the request
             by removing it from the database."""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            return True
        return False
