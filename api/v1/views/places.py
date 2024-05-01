#!/usr/bin/python3
"""Contains views for states."""
from flask import jsonify, abort, request
from markupsafe import escape
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=('GET', 'POST'), strict_slashes=False)
def places(city_id):
    """Handle GET and POST for places in a city."""
    city_id = escape(city_id)
    city = storage.get('City', city_id)

    if not city:
        abort(404)

    if request.method == 'POST':
        place_json = request.get_json(silent=True)
        if not place_json:
            abort(400, 'Not a JSON')
        if 'user_id' not in place_json:
            abort(400, 'Missing user_id')
        if 'name' not in place_json:
            abort(400, 'Missing name')

        place_json['city_id'] = city_id
        place = storage.cls_ref('Place')(**place_json)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def place(place_id):
    """Handle GET, PUT and DELETE for a place."""
    place = storage.get('Place', escape(place_id))

    if not place:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return {}

    if request.method == 'PUT':
        place_json = request.get_json(silent=True)
        if not place_json:
            abort(400, 'Not a JSON')
        for attr, val in place_json.items():
            if attr not in ['id', 'user_id',
                            'city_id', 'created_at', 'updated_at']:
                setattr(place, attr, val)
        storage.save()

    return jsonify(place.to_dict())
