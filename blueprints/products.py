# blueprints/products.py
from flask import Blueprint, request, jsonify
from models import Product, db

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'description': p.description,
        'prix': p.prix,
        'prix_de_vente': p.prix_de_vente(),  # Appel de la méthode du modèle
        'unites_par_carton': p.unites_par_carton
    } for p in products])

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    p = Product.query.get_or_404(id)
    return jsonify({
        'id': p.id,
        'nom': p.nom,
        'description': p.description,
        'prix': p.prix,
        'prix_de_vente': p.prix_de_vente,
        'unites_par_carton': p.unites_par_carton
    })

@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    p = Product.query.get_or_404(id)
    data = request.get_json()
    p.nom = data.get('nom', p.nom)
    p.description = data.get('description', p.description)
    p.prix = data.get('prix', p.prix)
    p.unites_par_carton = data.get('unites_par_carton', p.unites_par_carton)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
