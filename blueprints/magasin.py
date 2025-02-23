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
