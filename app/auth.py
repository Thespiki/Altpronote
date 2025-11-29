from flask import Blueprint, request, jsonify
from . import db
from .models import User, Role
from .auth_utils import encode_token, token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', Role.ELEVE.value)

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'username already exists'}), 400

    user = User(
        username=username,
        age=data.get('age'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address'),
        role=role,
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = encode_token(user.id)
    return jsonify({'message': 'user created', 'token': token, 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'invalid credentials'}), 401

    token = encode_token(user.id)
    return jsonify({'message': 'login successful', 'token': token, 'user': user.to_dict()}), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current authenticated user info."""
    user = User.query.get(request.user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    return jsonify({'user': user.to_dict()}), 200

