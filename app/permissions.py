from flask import Blueprint, request, jsonify
from . import db
from .models import User, Permission, Role
from .auth_utils import token_required, principal_required

permissions_bp = Blueprint('permissions', __name__, url_prefix='/permissions')


@permissions_bp.route('/', methods=['GET'])
def list_permissions():
    """List all available permissions."""
    perms = Permission.query.all()
    return jsonify({'permissions': [p.to_dict() for p in perms]}), 200


@permissions_bp.route('/<permission_id>', methods=['GET'])
def get_permission(permission_id):
    """Get a specific permission."""
    perm = Permission.query.get(permission_id)
    if not perm:
        return jsonify({'error': 'permission not found'}), 404
    return jsonify({'permission': perm.to_dict()}), 200


@permissions_bp.route('/', methods=['POST'])
@principal_required
def create_permission():
    """Create a new permission (principal only)."""
    data = request.get_json(force=True)
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'name required'}), 400

    if Permission.query.filter_by(name=name).first():
        return jsonify({'error': 'permission already exists'}), 400

    perm = Permission(name=name, description=description)
    db.session.add(perm)
    db.session.commit()

    return jsonify({'message': 'permission created', 'permission': perm.to_dict()}), 201


@permissions_bp.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_permissions(user_id):
    """Get permissions for a user."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'permissions': [p.to_dict() for p in user.permissions],
    }), 200


@permissions_bp.route('/user/<user_id>/grant', methods=['POST'])
@principal_required
def grant_permission(user_id):
    """Grant a permission to a user (principal only)."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404

    # Principal's permissions cannot be changed
    if user.role == Role.PRINCIPAL.value:
        return jsonify({'error': 'cannot modify principal permissions'}), 403

    data = request.get_json(force=True)
    permission_id = data.get('permission_id')

    if not permission_id:
        return jsonify({'error': 'permission_id required'}), 400

    perm = Permission.query.get(permission_id)
    if not perm:
        return jsonify({'error': 'permission not found'}), 404

    if perm in user.permissions:
        return jsonify({'error': 'user already has this permission'}), 400

    user.permissions.append(perm)
    db.session.commit()

    return jsonify({'message': 'permission granted', 'user': user.to_dict()}), 200


@permissions_bp.route('/user/<user_id>/revoke', methods=['POST'])
@principal_required
def revoke_permission(user_id):
    """Revoke a permission from a user (principal only)."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404

    # Principal's permissions cannot be changed
    if user.role == Role.PRINCIPAL.value:
        return jsonify({'error': 'cannot modify principal permissions'}), 403

    data = request.get_json(force=True)
    permission_id = data.get('permission_id')

    if not permission_id:
        return jsonify({'error': 'permission_id required'}), 400

    perm = Permission.query.get(permission_id)
    if not perm:
        return jsonify({'error': 'permission not found'}), 404

    if perm not in user.permissions:
        return jsonify({'error': 'user does not have this permission'}), 400

    user.permissions.remove(perm)
    db.session.commit()

    return jsonify({'message': 'permission revoked', 'user': user.to_dict()}), 200
