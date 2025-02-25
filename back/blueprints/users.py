# blueprints/users.py
from flask import Blueprint, request, jsonify
from models import User, db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/check_user', methods=['GET'])
def check_user():
    print("Vérification de l'existence d'utilisateurs...")
    user_count = User.query.count()  # Vérifie si des utilisateurs existent
    if user_count > 0:
        return 'login.html'
    else:
        return 'register.html'

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'nom': u.nom,
        'email': u.email,
        'role': u.role,
        'magasin_id': u.magasin_id
    } for u in users])

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    u = User.query.get_or_404(id)
    return jsonify({
        'id': u.id,
        'nom': u.nom,
        'email': u.email,
        'role': u.role,
        'magasin_id': u.magasin_id
    })

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    u = User.query.get_or_404(id)
    data = request.get_json()
    u.nom = data.get('nom', u.nom)
    u.email = data.get('email', u.email)
    u.role = data.get('role', u.role)
    u.magasin_id = data.get('magasin_id', u.magasin_id)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
