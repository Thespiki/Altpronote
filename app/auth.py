from flask import Blueprint, request, jsonify
from . import db
from .models import User, Role

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

    return jsonify({'message': 'user created', 'user': user.to_dict()}), 201


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

    # Placeholder: return basic info. Replace with token/session later.
    return jsonify({'message': 'login successful', 'user': user.to_dict()}), 200
