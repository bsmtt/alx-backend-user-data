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
    try:
        email = request.form['email']
        pasword = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, pasword)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"message": "email already registered"})
