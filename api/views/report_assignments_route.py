from models.report_assignments import ReportAssignment
from api.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route("/report_assignments", methods=['POST'])
def create_report_assignment(id):
    """Create a new report assignment."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'report_id' not in data or 'user_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    report_assignment = ReportAssignment(**data)
    storage.new(report_assignment)
    storage.save()

    return jsonify(report_assignment.to_dict()), 201

@app_views.route("/report_assignments/<id>", methods=['GET'])
def get_report_assignment(id):
    """Retrieve a report assignment by ID."""
    report_assignment = storage.get_by(ReportAssignment, id=id)
    if not report_assignment:
        return jsonify({"error": "Report assignment not found"}), 404
    return jsonify(report_assignment.to_dict()), 200

@app_views.route("/report_assignments", methods=['GET'])
def get_report_assignments():
    """Retrieve all report assignments."""
    report_assignments = storage.all(ReportAssignment)
    if not report_assignments:
        return jsonify({"error": "No report assignments found"}), 404
    return jsonify([ra.to_dict() for ra in report_assignments]), 200

app_views.route("/report-assignments/<assignment_id>", methods=['DELETE'])
def delete_report_assignment(assignment_id):
    """Delete a report assignment by ID."""
    report_assignment = storage.get_by(ReportAssignment, id=assignment_id)
    if not report_assignment:
        return jsonify({"error": "Report assignment not found"}), 404

    storage.delete(report_assignment)
    storage.save()

    return jsonify({}), 200

@app_views.route("/report_assignments/<id>", methods=['PUT'])
def update_report_assignment(id):
    """Update an existing report assignment."""
    report_assignment = storage.get_by(ReportAssignment, id=id)
    if not report_assignment:
        return jsonify({"error": "Report assignment not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(report_assignment, key, value)

    storage.save()

    return jsonify(report_assignment.to_dict()), 200