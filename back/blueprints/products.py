# blueprints/products.py
from flask import Blueprint, request, jsonify
from models import Product, db, Stock

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'prix': p.prix,
        'prix_de_vente': p.prix_de_vente, 
        'prix_unitaire': p.prix_unitaire,
        'unites_par_carton': p.unites_par_carton
    } for p in products])

@products_bp.route('/search', methods=['POST'])
def search_products():
    data = request.get_json()
    products = Product.query.filter(Product.nom.like(f'%{data["nom"]}%')).all()

    # Vérification du stock pour chaque produit
    for product in products:
        stock = Stock.query.filter_by(product_id=product.id).first()
        product.stock = stock.quantite if stock else 0
    
    return jsonify([{
        'id': p.id,
        'nom': p.nom,
        'prix': p.prix,
        'prix_de_vente': p.prix_de_vente, 
        'prix_unitaire': p.prix_unitaire,
        'unites_par_carton': p.unites_par_carton,
        'stock': p.stock
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

from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

@products_bp.route('/update/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        p = Product.query.get_or_404(id)
        data = request.get_json()


        # Mise à jour des attributs
        p.nom = data.get('nom', p.nom)
        p.prix = data.get('prix', p.prix)
        p.unites_par_carton = data.get('unites_par_carton', p.unites_par_carton)

        # Commit des changements
        db.session.commit()

        return jsonify({'message': 'product mis à jour avec succès'})
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback en cas d'erreur SQL
        return jsonify({'message': 'An error occurred while updating the product.', 'error': str(e)}), 500


@products_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        p = Product.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return jsonify({'message': 'product supprimé'})
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback en cas d'erreur SQL
        return jsonify({'message': 'An error occurred while deleting the product.', 'error': str(e)}), 500


@products_bp.route('/add', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        print(data)

        # Validation des données
        if not data.get('nom') or not data.get('prix') or not data.get('unites_par_carton'):
            return jsonify({'message': 'Invalid data. Ensure all fields are correct.'}), 400

        print(type(data['prix']))
        print(type(data['unites_par_carton']))


        # Création du produit
        p = Product(
            nom=data['nom'],
            prix=float(data['prix']),
            unites_par_carton=int(data['unites_par_carton'])
        )

        # Calcul du prix unitaire et du prix de vente
        prix_unitaire = p.prix / p.unites_par_carton
        p.prix_de_vente = round(float(prix_unitaire) + (float(prix_unitaire) * 0.4), 2)
        p.prix_unitaire = prix_unitaire

        print(p.prix_de_vente)
        print(prix_unitaire)
        print(p)
        # Ajout du produit à la base de données
        db.session.add(p)
        db.session.commit()

        return jsonify({'message': 'product ajouté avec succès'})
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback en cas d'erreur SQL
        return jsonify({'message': 'An error occurred while adding the product.', 'error': str(e)}), 500
