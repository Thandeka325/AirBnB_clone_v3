#!/usr/bin/python3
"""Flask app for AirBnB API"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(app_views, url_prefix="/api/v1")

# Enable CORS for all routes and allow requests from all origins (0.0.0.0)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return JSON response for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
