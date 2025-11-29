import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


def encode_token(user_id: str, expires_in: int = 3600) -> str:
    """Encode a JWT token for a user."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, current_app.config.get('SECRET_KEY', 'dev-secret'), algorithm='HS256')


def decode_token(token: str):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY', 'dev-secret'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """Decorator to require a valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'invalid token format'}), 401

        if not token:
            return jsonify({'error': 'token missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'invalid or expired token'}), 401

        # Attach user_id to request context
        request.user_id = payload.get('user_id')
        return f(*args, **kwargs)

    return decorated


def permission_required(permission_name: str):
    """Decorator to require a specific permission."""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            from .models import User
            user = User.query.get(request.user_id)
            if not user or not user.has_permission(permission_name):
                return jsonify({'error': 'insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


def principal_required(f):
    """Decorator to require principal role."""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        from .models import User, Role
        user = User.query.get(request.user_id)
        if not user or user.role != Role.PRINCIPAL.value:
            return jsonify({'error': 'principal access required'}), 403
        return f(*args, **kwargs)
    return decorated
