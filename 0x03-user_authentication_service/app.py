#!/usr/bin/env python3
"""
Flask app
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect, url_for

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """base route

    Returns:
        str: son response
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    email = request.form['email']
    pasword = request.form['password']
    try:
        AUTH.register_user(email, pasword)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    email = request.form['email']
    password = request.form['password']
    if not AUTH.valid_login(email, password):
        abort(401)
    
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    
    return response