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
    
    # Vérifier que les champs 'nom' et 'adresse' sont présents
    if not data or not data.get('nom') or not data.get('adresse'):
        return jsonify({'message': 'Nom et adresse du magasin sont requis'}), 400
    
    # Créer un nouveau magasin à partir du modèle SQLAlchemy
    new_magasin = Magasin(nom=data['nom'], adresse=data['adresse'])
    
    # Ajouter le nouveau magasin à la base de données
    db.session.add(new_magasin)
    db.session.commit()
    
    # Retourner une réponse de succès avec les détails du magasin ajouté
    return jsonify({
        'message': 'Magasin ajouté avec succès',
        'id': new_magasin.id,
        'nom': new_magasin.nom,
        'adresse': new_magasin.adresse
    }), 201


@magasins_bp.route('/<int:id>', methods=['GET'])
def get_magasin(id):
    m = Magasin.query.get_or_404(id)
    return jsonify({
        'id': m.id,
        'nom': m.nom,
        'adresse': m.adresse
    })

@magasins_bp.route('/update/<int:id>', methods=['PUT'])
def update_magasin(id):
    m = Magasin.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Aucune donnée fournie'}), 400

    try:
        if 'nom' in data:
            if not isinstance(data['nom'], str) or not data['nom'].strip():
                return jsonify({'error': 'Nom invalide'}), 400
            m.nom = data['nom'].strip()

        if 'adresse' in data:
            if not isinstance(data['adresse'], str) or not data['adresse'].strip():
                return jsonify({'error': 'Adresse invalide'}), 400
            m.adresse = data['adresse'].strip()

        db.session.commit()
        return jsonify({'message': 'Magasin mis à jour avec succès'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500


@magasins_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_magasin(id):
    m = Magasin.query.get_or_404(id)
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Magasin supprimé'})
