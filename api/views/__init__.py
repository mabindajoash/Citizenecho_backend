#!/usr/bin/python3
from flask import Blueprint
"""Blueprint"""

app_views = Blueprint('app_views', __name__, url_prefix='/api')
from api.views.users_route import *
from api.views.report_assignments_route import *
from api.views.reports_route import *
from api.views.inquiries_route import *
