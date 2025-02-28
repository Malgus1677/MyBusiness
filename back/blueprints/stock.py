# blueprints/stock.py
from flask import Blueprint, request, jsonify
from models import Stock, db
from flask_jwt_extended import jwt_required

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/', methods=['GET'])
def get_stock():
    stocks = Stock.query.all()
    return jsonify([{
        'id': s.id,
        'product_id': s.product_id,
        'magasin_id': s.magasin_id,
        'quantite': s.quantite
    } for s in stocks])

@stock_bp.route('/<int:id>', methods=['GET'])
def get_stock_item(id):
    s = Stock.query.get_or_404(id)
    return jsonify({
        'id': s.id,
        'product_id': s.product_id,
        'magasin_id': s.magasin_id,
        'quantite': s.quantite
    })

@stock_bp.route('/<int:id>', methods=['PUT'])
def update_stock(id):
    s = Stock.query.get_or_404(id)
    data = request.get_json()
    s.product_id = data.get('product_id', s.product_id)
    s.magasin_id = data.get('magasin_id', s.magasin_id)
    s.quantite = data.get('quantite', s.quantite)
    db.session.commit()
    return jsonify({'message': 'Stock updated successfully'})

@stock_bp.route('/<int:id>', methods=['DELETE'])
def delete_stock(id):
    s = Stock.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Stock deleted successfully'})

@stock_bp.route('/api/stock', methods=['POST'])
@jwt_required()  # Sécurisez la route avec l'authentification JWT
def add_stock():
    try:
        # Récupérer les données envoyées dans la requête
        data = request.get_json()

        magasin_id = data.get('store_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        # Valider les données
        if not magasin_id or not product_id or not quantity:
            return jsonify({"message": "Tous les champs sont requis."}), 400

        # Vérifier si le magasin existe
        magasin = Magasin.query.get(magasin_id)
        if not magasin:
            return jsonify({"message": "Le magasin spécifié n'existe pas."}), 404

        # Vérifier si le produit existe
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Le produit spécifié n'existe pas."}), 404

        # Créer un nouvel enregistrement de stock
        stock_item = Stock(magasin_id=magasin_id, product_id=product_id, quantite=quantity)

        # Ajouter et committer dans la base de données
        db.session.add(stock_item)
        db.session.commit()

        return jsonify({"message": "Réception de stock ajoutée avec succès."}), 201

    except Exception as e:
        # En cas d'erreur, retourner le message d'erreur
        db.session.rollback()
        return jsonify({"message": f"Erreur lors de l'ajout du stock : {str(e)}"}), 500
