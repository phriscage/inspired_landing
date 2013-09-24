#!/usr/bin/python
"""
UI bootstrap file
"""
from flask import Flask, jsonify
import sys
import os
import argparse

#sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../lib')
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../conf')

import landing
import users.views

def bootstrap(**kwargs):
    """bootstraps the application. can handle setup here"""
    app = Flask(__name__, static_url_path='', static_folder='./static')
    app.register_blueprint(landing.app)
    app.register_blueprint(users.views.users, url_prefix="/users")
    app.debug = True
    app.run(host=kwargs['host'], port=kwargs['port'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Hostname or IP address",
        dest="host", type=str, default='0.0.0.0')
    parser.add_argument("--port", help="Port number",
        dest="port", type=int, default=8000)
    kwargs = parser.parse_args()
    bootstrap(**kwargs.__dict__)

