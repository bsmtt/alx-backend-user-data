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
