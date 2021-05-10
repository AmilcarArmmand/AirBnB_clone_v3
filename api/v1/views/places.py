#!/usr/bin/python3
"""
Flask route that returns status of state JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_from_city(city_id=None):
    """places not linked to an object
    """

    given_city = storage.get('City', city_id)
    if given_city is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = [place.to_dict() for place
                      in given_city.places]
        return jsonify(all_places)
    # ====================================================================
    if request.method == 'POST':
        json_req = request.get_json()
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in request.get_json():
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        if storage.get('User', json_req['user_id']) is None:
            abort(404)
    place = Place(**request.get_json())
    setattr(place, "city_id", city_id)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_places(place_id=None):

    given_place = storage.get('Place', place_id)
    if given_place is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(given_place.to_dict())
    if request.method == 'DELETE':
        given_place.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at', 'user_id']:
                setattr(given_place, attr, value)
    given_place.save()
    return jsonify(given_place.to_dict())
