from models import storage
from flask import make_response, jsonify, abort, request
from api.views import app_views
from models.users import User
from models.report_assignments import ReportAssignment

@app_views.route("/users/<id>", methods=['GET'])
def get_user(id):
    """Retrieve a user by ID."""
    user = storage.get_by(User, id=id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@app_views.route("/users", methods=['GET'])
def get_users():
    """Retrieve all users."""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users]), 200
    if not users:
        return jsonify({"error": "No users found"}), 404

@app_views.route("/users", methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data or 'password' not in data or 'name' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    
    return jsonify(new_user.to_dict()), 201

@app_views.route("/users/<id>", methods=['PUT'])
def update_user(id):
    """Update an existing user."""
    user = storage.get_by(User, id=id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    storage.save()
    
    return jsonify(user.to_dict()), 200

@app_views.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    """Delete a user by ID."""
    user = storage.get_by(User, id=id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    storage.delete(user)
    storage.save()
    
    return jsonify({}), 200

@app_views.route("/api/users/<id>/assigned-reports", methods=['GET'])
def get_assigned_reports(user_id):
    """Retrieve all reports assigned to a user."""
    user = storage.get_by(User, id=id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    assigned_reports = storage.get_all_by(ReportAssignment, user_id=user_id)
    if not assigned_reports:
        return jsonify({"error": "No assigned reports found"}), 404
    
    return jsonify([report.to_dict() for report in assigned_reports]), 200
