from models import storage
from api.views import app_views
from models.reports import Report
from flask import jsonify, request

@app_views.route("/reports/<id>", methods=['GET'])
def get_report(id):
    """Retrieve a report by ID."""
    report = storage.get_by(Report, id=id)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report.to_dict()), 200

@app_views.route("/reports", methods=['GET'])
def get_reports():
    """Retrieve all reports."""
    reports = storage.all(Report)
    if not reports:
        return jsonify({"error": "No reports found"}), 404
    return jsonify([report.to_dict() for report in reports.values()]), 200

@app_views.route("/reports", methods=['POST'])
def create_report():
    """Create a new report."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'title' not in data or 'description' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_report = Report(**data)
    storage.new(new_report)
    storage.save()

    return jsonify(new_report.to_dict()), 201

@app_views.route("/reports/<id>", methods=['PUT'])
def update_report(id):
    """Update an existing report."""
    report = storage.get_by(Report, id=id)
    if not report:
        return jsonify({"error": "Report not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(report, key, value)

    storage.save()

    return jsonify(report.to_dict()), 200

@app_views.route("/reports/<id>", methods=['DELETE'])
def delete_report(id):
    """Delete a report by ID."""
    report = storage.get_by(Report, id=id)
    if not report:
        return jsonify({"error": "Report not found"}), 404

    storage.delete(report)
    storage.save()

    return jsonify({}), 200

@app_views.route("/reports/<id>/assignments", methods=['GET'])
def get_report_assignments(id):
    """Retrieve all assignments for a specific report."""
    report = storage.get_by(Report, id=id)
    if not report:
        return jsonify({"error": "Report not found"}), 404

    assignments = report.assignments
    if not assignments:
        return jsonify({"error": "No assignments found for this report"}), 404

    return jsonify([assignment.to_dict() for assignment in assignments]), 200

@app_views.route("/reports/<id>/assignments", methods=['POST'])
def assign_report(id):
    """Assign a report to a user."""
    report = storage.get_by(Report, id=id)
    if not report:
        return jsonify({"error": "Report not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    from models.report_assignments import ReportAssignment
    assignment = ReportAssignment(report_id=id, user_id=data['user_id'])
    storage.new(assignment)
    storage.save()

    return jsonify(assignment.to_dict()), 201