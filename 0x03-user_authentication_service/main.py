#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user with the given email and password."""
    payload = {'email': email, 'password': password}
    response = requests.post(f"{BASE_URL}/users", data=payload)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the provided email and password,
         expecting authentication failure."""
    payload = {'email': email, 'password': password}
    response = requests.post(f"{BASE_URL}/sessions", data=payload)
    assert response.status_code == 401


def profile_unlogged():
    """Access the profile page without logging in,
         expecting a 403 Forbidden response."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Log in with the given email and password,
         returning the session ID."""
    payload = {'email': email, 'password': password}
    response = requests.post(f"{BASE_URL}/sessions", data=payload)
    assert response.status_code == 200
    session_id = response.cookies.get('session_id')
    assert session_id is not None
    return session_id


def profile_logged(session_id: str) -> None:
    """Access the profile page with the provided session ID."""
    cookies = {'session_id': session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200


def log_out(session_id):
    """Log out the user with the given session ID."""
    cookies = {'session_id': session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Request a reset token for the password associated
         with the provided email."""
    payload = {'email': email}
    response = requests.post(f"{BASE_URL}/reset_password", data=payload)
    assert response.status_code == 200
    data = response.json()
    # extract json data from the response
    reset_token = data.get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password associated with the provided email
         using the reset token and new password."""
    payload = {'email': email, 'reset_token': reset_token,
               'new_password': new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=payload)
    assert response.status_code == 200


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
