#!/usr/bin/env python3
"""module for SessionExpAuth's class"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration authentication class"""
    def __init__(self):
        """Initialize SessionExpAuth"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID linked to a session, considering expiration"""
        if not session_id:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id', None)
        if 'created_at' not in session_dict:
            return None
        created_at = session_dict['created_at']
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        return session_dict.get('user_id')
