#!/usr/bin/python3
"""Contains views for cities."""
from flask import jsonify, abort, request
from markupsafe import escape
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=('GET', 'POST'), strict_slashes=False)
def cities(state_id):
    """Retrieve list of cities in a state."""
    state_id = escape(state_id)
    state = storage.get('State', state_id)

    if not state:
        abort(404)

    if request.method == 'POST':
        city_json = request.get_json(silent=True)

        if not city_json:
            abort(400, 'Not a JSON')
        if 'name' not in city_json:
            abort(400, 'Missing name')

        city_json['state_id'] = state_id
        city = storage.cls_ref('City')(**city_json)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def city(city_id):
    """Get a city."""
    city = storage.get('City', escape(city_id))

    if not city:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return {}

    if request.method == 'PUT':
        city_json = request.get_json(silent=True)
        if not city_json:
            abort(400, 'Not a JSON')
        for attr, val in city_json.items():
            if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, attr, val)
        storage.save()

    return jsonify(city.to_dict())
