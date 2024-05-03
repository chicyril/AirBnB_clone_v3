#!/usr/bin/python3
"""
Module containing a flack instance.
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close_db(exception):
    """Close or remove the database session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 status-code response."""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
