#!/usr/bin/python3
"""
Initialize the Blueprint for API v1 views.
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views (PEP8 will complain about wildcard import, but it's required)
from api.v1.views.index import *

