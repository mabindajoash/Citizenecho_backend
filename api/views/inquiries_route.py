from models.inquiries import Inquiry
from models import storage
from api.views import app_views
from flask import jsonify, request


@app_views.route("/inquiries/<id>", methods=['GET'])
def get_inquiry(id):
    """Retrieve an inquiry by ID."""
    inquiry = storage.get_by(Inquiry, id=id)
    if not inquiry:
        return jsonify({"error": "Inquiry not found"}), 404
    return jsonify(inquiry.to_dict()), 200

@app_views.route("/inquiries", methods=['GET'])
def get_inquiries():
    """Retrieve all inquiries."""
    inquiries = storage.all(Inquiry)
    if not inquiries:
        return jsonify({"error": "No inquiries found"}), 404
    return jsonify([inquiry.to_dict() for inquiry in inquiries.values()]), 200

@app_views.route("/inquiries", methods=['POST'])
def create_inquiry():
    """Create a new inquiry."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data or 'email' not in data or 'message' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_inquiry = Inquiry(**data)
    storage.new(new_inquiry)
    storage.save()

    return jsonify(new_inquiry.to_dict()), 201

@app_views.route("/inquiries/<id>", methods=['PUT'])
def update_inquiry(id):
    """Update an existing inquiry."""
    inquiry = storage.get_by(Inquiry, id=id)
    if not inquiry:
        return jsonify({"error": "Inquiry not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(inquiry, key, value)

    storage.save()

    return jsonify(inquiry.to_dict()), 200

@app_views.route("/inquiries/<id>", methods=['DELETE'])
def delete_inquiry(id):
    """Delete an inquiry by ID."""
    inquiry = storage.get_by(Inquiry, id=id)
    if not inquiry:
        return jsonify({"error": "Inquiry not found"}), 404

    storage.delete(inquiry)
    storage.save()

    return jsonify({}), 200
