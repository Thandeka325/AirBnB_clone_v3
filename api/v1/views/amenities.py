#!/usr/bin/python3
"""
API actions for Amenity objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieves a specific Amenity object by ID
    """
    fetched_obj = storage.get(Amenity, amenity_id)
    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Creates a new Amenity object
    """
    am_json = request.get_json()
    if not am_json:
        abort(400, 'Not a JSON')
    if "name" not in am_json:
        abort(400, 'Missing name')

    new_am = Amenity(**am_json)
    new_am.save()
    return jsonify(new_am.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    Updates an existing Amenity object
    """
    fetched_obj = storage.get(Amenity, amenity_id)
    if fetched_obj is None:
        abort(404)

    am_json = request.get_json()
    if not am_json:
        abort(400, 'Not a JSON')

    for key, val in am_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()
    return jsonify(fetched_obj.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    Deletes an Amenity by ID
    """
    fetched_obj = storage.get(Amenity, amenity_id)
    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()
    return jsonify({}), 200
