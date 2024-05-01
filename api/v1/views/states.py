#!/usr/bin/python3
"""Contains views for states related endpoints."""
from flask import jsonify, abort, request
from markupsafe import escape
from api.v1.views import app_views
from models import storage


@app_views.route('/states',
                 methods=('GET', 'POST'), strict_slashes=False)
def states():
    """Get states infos or create a state."""
    if request.method == 'POST':
        state_json = request.get_json(silent=True)

        if not state_json:
            abort(400, 'Not a JSON')

        if 'name' not in state_json:
            abort(400, 'Missing name')

        state = storage.cls_ref("State")(**state_json)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201

    return jsonify([state.to_dict()
                    for state in storage.all('State').values()])


@app_views.route('/states/<state_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def state(state_id):
    """Get or update a state's info, or delete the state."""
    state = storage.get('State', escape(state_id))

    if not state:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return {}

    if request.method == 'PUT':
        state_json = request.get_json(silent=True)
        if not state_json:
            abort(400, 'Not a JSON')
        for attr, val in state_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(state, attr, val)
        storage.save()

    return jsonify(state.to_dict())
