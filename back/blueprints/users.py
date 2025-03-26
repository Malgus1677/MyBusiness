from flask import Blueprint, request, jsonify, abort
from models import User, db
import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Vérification de l'existence d'utilisateurs, redirection vers login ou registre
@users_bp.route('/check_user', methods=['GET'])
def check_user():
    user_count = User.query.count()  # Vérifie si des utilisateurs existent
    if user_count > 0:
        return 'login.html'
    else:
        return 'register.html'

# Récupération de tous les utilisateurs (nécessite l'authentification)
@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    print('users', users)
    
    return jsonify([{
        'id': u.id,
        'nom': u.nom,
        'prenom' : u.prenom,
        'username': u.username,
        'role': u.role,
        'magasin_id': u.magasin_id
    } for u in users])

# Récupération d'un utilisateur par ID (nécessite l'authentification)
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):

    
    u = User.query.get_or_404(id)
    return jsonify({
        'id': u.id,
        'nom': u.nom,
        'prenom' : u.prenom,
        'username': u.username,
        'role': u.role,
        'magasin_id': u.magasin_id
    })

# Mise à jour d'un utilisateur (nécessite l'authentification)
@users_bp.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    u = User.query.get_or_404(id)
    data = request.get_json()

    print(data)

    # Validation des données d'entrée
    if 'username' in data and not isinstance(data['username'], str):
        abort(400, description="L'username doit être une chaîne de caractères.")
    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    u.password = hashed_password.decode('utf-8')

    u.nom = data.get('nom', u.nom)
    u.prenom = data.get('prenom', u.prenom)
    u.username = data.get('username', u.username)
    u.role = data.get('role', u.role)
    u.magasin_id = data.get('magasin', u.magasin_id)

    db.session.commit()
    return jsonify({'message': 'Utilisateur mis à jour avec succès'})

# Suppression d'un utilisateur (nécessite l'authentification)
@users_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé avec succès'})

# Création d'un nouvel utilisateur (POST avec vérification de sécurité)
@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    print('data', data)
    
    # Vérification des données envoyées
    if not data or not data.get('nom') or not data.get('prenom') or not data.get('username') or not data.get('password'):
        abort(400, description="Les champs 'nom', 'prenom', 'username' et 'mot de passe' sont requis.")
    
    # Vérification si l'username existe déjà
    if User.query.filter_by(username=data['username']).first():
        abort(400, description="Le nom d'utilisateur est déjà utilisé.")
    
    # Récupération du rôle et du magasin_id
    role = data.get('role', 'user')  # Valeur par défaut 'user' si non fourni
    magasin_id = data.get('magasin_id', None)  # Valeur par défaut None si non fourni
    
    # Validation du rôle
    if role not in ['admin', 'manager', 'employee']:
        return jsonify({'message': 'Rôle invalide'}), 400
    
    # Validation du magasin_id pour les rôles 'manager' et 'employee'
    if role in ['manager', 'employee'] and not magasin_id:
        return jsonify({'message': 'Un magasin doit être sélectionné pour ce rôle'}), 400
    
    # Hachage du mot de passe avec bcrypt
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Si le rôle est 'admin', le magasin_id doit être None
    if role == 'admin':
        magasin_id = None
    
    # Création de l'utilisateur
    new_user = User(
        nom=data['nom'],
        prenom=data['prenom'],
        username=data['username'],
        password=hashed_password.decode('utf-8'),
        role=role,
        magasin_id=magasin_id
    )
   
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'Utilisateur ajouté avec succès',
        'id': new_user.id,
        'nom': new_user.nom,
        'prenom': new_user.prenom,
        'username': new_user.username,
        'role': new_user.role,
        'magasin_id': new_user.magasin_id
    }), 201

# Vérification du mot de passe lors de la connexion (POST)
@users_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    print('Données de connexion :', data)

    user = User.query.filter_by(username=data['username']).first()
    print('Utilisateur :', user)

    # Vérifier si l'utilisateur existe
    if not user:
        abort(401, description="Nom d'utilisateur incorrect.")
    
    # Vérifier si le mot de passe est correct
    password_matches = bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8'))
    print('Mot de passe correct :', password_matches)
    if not password_matches:
        abort(401, description="Mot de passe incorrect.")

    print('Utilisateur connecté :', user.id)
    access_token = create_access_token(identity=user.role)
    print('Access token :', access_token)

    return jsonify({
        'access_token': access_token,
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'magasin_id': user.magasin_id
    }), 200
