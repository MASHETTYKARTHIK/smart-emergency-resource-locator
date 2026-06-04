from flask import Blueprint, jsonify, request

from .service import EmergencyService

emergency_bp = Blueprint("emergency", __name__)
service = EmergencyService()


@emergency_bp.route("/nearest", methods=["GET"])
def get_nearest():
    """
    GET /api/emergency/nearest
    Query parameters:
    - lat (float)
    - lon (float)
    - type (hospital | police | fire_station | blood_bank)
    """
    try:
        lat = request.args.get("lat", type=float)
        lon = request.args.get("lon", type=float)
        resource_type = request.args.get("type")

        if lat is None or lon is None or not resource_type:
            return jsonify(
                {"error": "Missing required parameters: lat, lon, type"}
            ), 400

        valid_types = ["hospital", "police", "fire_station", "blood_bank"]
        if resource_type not in valid_types:
            return jsonify(
                {"error": f"Invalid type. Must be one of: {', '.join(valid_types)}"}
            ), 400

        result = service.get_nearest_resource(lat, lon, resource_type)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
