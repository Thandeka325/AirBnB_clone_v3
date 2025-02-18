#!/usr/bin/python3
"""
API for Places view object
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending on the JSON in the body"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data == {} or all(isinstance(value, list) and len(value) == 0
                         for value in data.values()):
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places = []

    if data.get('states'):
        states = [storage.get(State, state_id) for state_id in data['states']
                  if storage.get(State, state_id)]
        for state in states:
            places.extend([place for city in state.cities
                           for place in city.places])

    if data.get('cities'):
        cities = [storage.get(City, city_id) for city_id in data['cities']
                  if storage.get(City, city_id)]
        places.extend([place for city in cities for place in city.places])

    if not places:
        places = storage.all(Place).values()

    if data.get('amenities'):
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in data['amenities']]
        places = [place for place in places
                  if all(amenity in place.amenities for amenity in amenities)]

    return jsonify([{key: value for key, value in place.to_dict().items()
                     if key != 'amenities'} for place in places])
