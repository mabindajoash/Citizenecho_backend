#!/usr/bin/python3

from flask import Flask, jsonify, make_response
from api.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SECRET_KEY'] = 'citizenecho_api'

@app.teardown_appcontext
def close_db(error):
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': "Bad request. check documentation"}), 400)

@app.errorhandler(403)
def unauthorized(error):
    return make_response(jsonify({'error': "unauthorized access"}), 403)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5000', threaded=True, debug=True)