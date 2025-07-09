from flask import Blueprint, request, jsonify
from models.users import User
from models import storage
from api.views import app_views

@app_views.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = storage.get_by(User, email=email)

    if user and user.check_password(password):
        return jsonify({
            "message": "Login successful",
            "user": user.to_dict()
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401
