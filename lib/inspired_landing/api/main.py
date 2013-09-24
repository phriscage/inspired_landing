#!/usr/bin/python
"""
UI bootstrap file
"""
from flask import Flask, jsonify
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../../lib')
sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../../conf')

from inspired_landing_config import SQLALCHEMY_DATABASE_URI

from inspired_landing.lib.database import init_engine, db_session

def create_app(uri):
    """ dynamically create the app """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(500)
    def default_error_handle(error=None):
        """ handle all errors with json output """
        return jsonify(error=error.code, message=error.message, success=False),\
            error.code

    from inspired_landing.api.users.views import users
    app.register_blueprint(users, url_prefix="/users")
    return app


def bootstrap(**kwargs):
    """bootstraps the application. can handle setup here"""
    app = create_app(SQLALCHEMY_DATABASE_URI)
    app.debug = True
    app.run(host=kwargs['host'], port=kwargs['port'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Hostname or IP address",
        dest="host", type=str, default='0.0.0.0')
    parser.add_argument("--port", help="Port number",
        dest="port", type=int, default=8001)
    kwargs = parser.parse_args()
    bootstrap(**kwargs.__dict__)

