#!/usr/bin/python3
"""
Flask route that returns status of state JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def review_from_place(place_id=None):
    """reveiws from place object
    """

    given_place = storage.get('Place', place_id)
    if given_place is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_reviews = [review.to_dict() for review
                       in given_place.reviews]
        return jsonify(all_reviews)
    # ====================================================================
    if request.method == 'POST':
        json_req = request.get_json()
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in request.get_json():
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if 'text' not in request.get_json():
            return make_response(jsonify({'error': 'Missing text'}), 400)
        if storage.get('User', json_req['user_id']) is None:
            abort(404)
    review = Review(**request.get_json())
    setattr(review, "place_id", place_id)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_reviews(review_id=None):

    given_review = storage.get('Review', review_id)
    if given_review is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(given_review.to_dict())
    if request.method == 'DELETE':
        given_review.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at',
                            'user_id', 'place_id']:
                setattr(given_review, attr, value)
    given_review.save()
    return jsonify(given_review.to_dict())
