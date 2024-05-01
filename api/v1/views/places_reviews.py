#!/usr/bin/python3
"""Contains views for states."""
from flask import jsonify, abort, request
from markupsafe import escape
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=('GET', 'POST'), strict_slashes=False)
def place_reviews(place_id):
    """Handle GET and POST for a places' reviews."""
    place_id = escape(place_id)
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    if request.method == 'POST':
        review_json = request.get_json(silent=True)
        if not review_json:
            abort(400, 'Not a JSON')
        if 'user_id' not in review_json:
            abort(400, 'Missing user_id')
        if not storage.get('User', escape(review_json['user_id'])):
            abort(404)
        if 'text' not in review_json:
            abort(400, 'Missing text')
        review_json['place_id'] = place_id
        review = storage.cls_ref('Review')(**review_json)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict())

    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def review(review_id):
    """Handle Get, post and delete for a review request."""
    review = storage.get('Review', escape(review_id))

    if not review:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return {}

    if request.method == 'PUT':
        review_json = request.get_json(silent=True)
        if not review_json:
            abort(400, 'Not a JSON')
        for attr, val in review_json.items():
            if attr not in ['id', 'user_id',
                            'place_id', 'created_at', 'updated_at']:
                setattr(review, attr, val)
        storage.save()

    return jsonify(review.to_dict())
