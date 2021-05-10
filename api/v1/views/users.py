#!/usr/bin/python3
"""
Flask route that returns status of state JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users_unlinked():
    """users not linked to an object
    """
    if request.method == 'GET':
        all_users = [user.to_dict() for user in storage.
                     all("User").values()]
        return (jsonify(all_users), 200)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'email' not in request.get_json():
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in request.get_json():
            return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def users_linked(user_id=None):
    """ users alread linked to an object """
    given_user = storage.get('User', user_id)
    if given_user is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(given_user.to_dict())

    if request.method == 'DELETE':
        given_user.delete()
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'PUT':
        if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(given_user, attr, value)
    given_user.save()
    return jsonify(given_user.to_dict())
