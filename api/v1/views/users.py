#!/usr/bin/python3
"""Contains views for all user related endpoints."""
from flask import jsonify, abort, request
from markupsafe import escape
from api.v1.views import app_views
from models import storage


@app_views.route('/users',
                 methods=('GET', 'POST'), strict_slashes=False)
def users():
    """Retrieve all users in the database."""
    if request.method == 'POST':
        user_json = request.get_json(silent=True)

        if not user_json:
            abort(400, 'Not a JSON')
        if 'email' not in user_json:
            abort(400, 'Missing email')
        if 'password' not in user_json:
            abort(400, 'Missing password')

        user = storage.cls_ref('User')(**user_json)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201

    return jsonify([user.to_dict() for user in storage.all('User').values()])


@app_views.route('/users/<user_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def user(user_id):
    """Get a specific user with whose id is user_id."""
    user = storage.get('User', escape(user_id))

    if not user:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return {}

    if request.method == 'PUT':
        user_json = request.get_json(silent=True)
        if not user_json:
            abort(400, 'Not a JSON')
        for attr, val in user_json.items():
            if attr not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, attr, val)
        storage.save()

    return jsonify(user.to_dict())
