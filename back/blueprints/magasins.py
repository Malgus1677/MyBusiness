# blueprints/magasins.py
from flask import Blueprint, request, jsonify
from models import Magasin, db

magasins_bp = Blueprint('magasins', __name__, url_prefix='/magasins')

@magasins_bp.route('/', methods=['GET'])
def get_magasins():
    magasins = Magasin.query.all()
    return jsonify([{
        'id': m.id,
        'nom': m.nom,
        'adresse': m.adresse
    } for m in magasins])

@magasins_bp.route('/add', methods=['POST'])
def ajouter_magasin():
    data = request.get_json()  # Récupérer les données JSON envoyées depuis le frontend
    
    # Vérification si les champs 'nom' et 'adresse' existent dans la requête
    if not data.get('nom') or not data.get('adresse'):
        return jsonify({'message': 'Nom et adresse du magasin sont requis'}), 400
    
    # Créer un nouvel ID pour le magasin
    new_id = len(magasins) + 1
    
    # Créer un nouveau magasin
    new_magasin = {
        "id": new_id,
        "nom": data['nom'],
        "adresse": data['adresse']
    }
    
    # Ajouter le magasin à la liste
    magasins.append(new_magasin)
    
    # Retourner une réponse de succès avec les détails du magasin ajouté
    return jsonify({
        'message': 'Magasin ajouté avec succès',
        'id': new_magasin['id'],
        'nom': new_magasin['nom'],
        'adresse': new_magasin['adresse']
    }), 201

@magasins_bp.route('/<int:id>', methods=['GET'])
def get_magasin(id):
    m = Magasin.query.get_or_404(id)
    return jsonify({
        'id': m.id,
        'nom': m.nom,
        'adresse': m.adresse
    })

@magasins_bp.route('/<int:id>', methods=['PUT'])
def update_magasin(id):
    m = Magasin.query.get_or_404(id)
    data = request.get_json()
    m.nom = data.get('nom', m.nom)
    m.adresse = data.get('adresse', m.adresse)
    db.session.commit()
    return jsonify({'message': 'Magasin updated successfully'})

@magasins_bp.route('/<int:id>', methods=['DELETE'])
def delete_magasin(id):
    m = Magasin.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Magasin deleted successfully'})
