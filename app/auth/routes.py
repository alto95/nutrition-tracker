from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from app.auth import auth_bp

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    return jsonify({"message": "Auth routes working"}), 200
