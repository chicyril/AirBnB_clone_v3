#!/usr/bin/python3
"""Contains views for amenities."""
from flask import jsonify, abort, request
from markupsafe import escape
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities',
                 methods=('GET', 'POST'), strict_slashes=False)
def amenities():
    """Retrieve list of amenities."""
    if request.method == 'POST':
        amenity_json = request.get_json(silent=True)

        if not amenity_json:
            abort(400, 'Not a JSON')
        if 'name' not in amenity_json:
            abort(400, 'Missing name')

        amenity = storage.cls_ref('Amenity')(**amenity_json)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    return jsonify([amenity.to_dict()
                    for amenity in storage.all('Amenity').values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def amenity(amenity_id):
    """Get an amenity."""
    amenity = storage.get('Amenity', escape(amenity_id))

    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return {}

    if request.method == 'PUT':
        amenity_json = request.get_json(silent=True)
        if not amenity_json:
            abort(400, 'Not a JSON')
        for attr, val in amenity_json.items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, attr, val)
        storage.save()

    return jsonify(amenity.to_dict())
