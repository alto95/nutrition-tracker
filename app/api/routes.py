from flask import jsonify, request
from app.api import api_bp

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200
