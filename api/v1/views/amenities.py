#!/usr/bin/python3
"""
Flask route that returns status of state JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities_unlinked():
    """amenities not linked to an object
    """
    if request.method == 'GET':
        all_amenity = [amenity.to_dict() for amenity in storage.
                       all("Amenity").values()]
        return (jsonify(all_amenity), 200)
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_linked(amenity_id=None):
    # Checks if city exists / retrieves the city object requested by ID
    given_amenity = storage.get('Amenity', amenity_id)
    if given_amenity is None:
        abort(404, 'Not found')
    # =================================================================
    if request.method == 'GET':
        return jsonify(given_amenity.to_dict())

    if request.method == 'DELETE':
        given_amenity.delete()
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(given_amenity, attr, value)
    given_amenity.save()
    return jsonify(given_amenity.to_dict())
