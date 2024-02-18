#!/usr/bin/env python3
"""A simple Flask application for user registration."""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


auth = Auth()


app = Flask(__name__)


@app.route("/")
def home():
    """Render the home page."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Handle user registration."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login() -> str:
    """ handle sessions """
    email = request.form.get('email')
    password = request.form.get('password')
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
