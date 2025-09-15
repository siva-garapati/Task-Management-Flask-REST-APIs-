from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "User already exists"}), 400

        # Create user
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "Registration successful"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Basic validation
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check credentials
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Create JWT token (never expires if configured in app config)
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"msg": "Login successful", "token": access_token})

        return jsonify({"msg": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
