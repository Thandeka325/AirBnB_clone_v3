#!/usr/bin/python3
"""
API endpoints for State objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    :return: JSON of all states
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    retrieves a specific State object by ID
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    creates a new State object
    """
    state_json = request.get_json()
    if not state_json:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state_json = request.get_json()
    if not state_json:
        abort(400, 'Not a JSON')

    for key, value in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes a State by ID
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200
