#!/usr/bin/python3
"""Places view for API"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves Place objects based on filters from JSON request body"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if not data or (
        not data.get("states") and
        not data.get("cities") and
        not data.get("amenities")
    ):
        # If no filters are provided, return all Places
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places]), 200

    places_set = set()

    # Get places linked to provided State IDs
    state_ids = data.get("states", [])
    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places_set.update(city.places)

    # Get places linked to provided City IDs
    city_ids = data.get("cities", [])
    for city_id in city_ids:
        city = storage.get(City, city_id)
        if city:
            places_set.update(city.places)

    # Convert set to list for filtering
    places_list = list(places_set)

    # Filter by amenities (include places that have all amenities in the list)
    amenity_ids = data.get("amenities", [])
    if amenity_ids:
        places_list = [place for place in places_list if all(
            storage.get(Amenity, amenity_id) in place.amenities
            for amenity_id in amenity_ids
        )]

    return jsonify([place.to_dict() for place in places_list]), 200
