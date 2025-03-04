from flask import Blueprint, request, jsonify
from models import Sales, Product, User, Magasin, db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/', methods=['GET'])
def get_sales():
    try:
        sales = Sales.query.all()
        return jsonify([{
            'id': s.id,
            'user_id': s.user_id,
            'product_id': s.product_id,
            'magasin_id': s.magasin_id,
            'quantite': s.quantite,
            'montant': s.montant,
            'date': s.date.isoformat()
        } for s in sales])
    
    except SQLAlchemyError as e:
        return jsonify({'message': 'An error occurred while fetching the sales.', 'error': str(e)}), 500

@sales_bp.route('/<int:id>', methods=['GET'])
def get_sale(id):
    try:
        s = Sales.query.get_or_404(id)
        return jsonify({
            'id': s.id,
            'user_id': s.user_id,
            'product_id': s.product_id,
            'magasin_id': s.magasin_id,
            'quantite': s.quantite,
            'montant': s.montant,
            'date': s.date.isoformat()
        })
    
    except SQLAlchemyError as e:
        return jsonify({'message': 'An error occurred while fetching the sale.', 'error': str(e)}), 500

@sales_bp.route('/<int:id>', methods=['PUT'])
def update_sale(id):
    try:
        s = Sales.query.get_or_404(id)
        data = request.get_json()

        # Validation des données
        if not isinstance(data.get('quantite'), int) or data.get('quantite') < 0:
            return jsonify({'message': 'Invalid quantity. It must be a non-negative integer.'}), 400
        
        if not isinstance(data.get('montant'), (int, float)) or data.get('montant') < 0:
            return jsonify({'message': 'Invalid amount. It must be a non-negative number.'}), 400

        s.user_id = data.get('user_id', s.user_id)
        s.product_id = data.get('product_id', s.product_id)
        s.magasin_id = data.get('magasin_id', s.magasin_id)
        s.quantite = data.get('quantite', s.quantite)
        s.montant = data.get('montant', s.montant)
        
        # Optionnel : mettre à jour la date si fournie
        if data.get('date'):
            try:
                s.date = datetime.fromisoformat(data.get('date'))
            except ValueError:
                return jsonify({'message': 'Invalid date format. Use ISO 8601 format.'}), 400

        db.session.commit()
        return jsonify({'message': 'Sale updated successfully'})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating the sale.', 'error': str(e)}), 500

@sales_bp.route('/<int:id>', methods=['DELETE'])
def delete_sale(id):
    try:
        s = Sales.query.get_or_404(id)
        db.session.delete(s)
        db.session.commit()
        return jsonify({'message': 'Sale deleted successfully'})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the sale.', 'error': str(e)}), 500

@sales_bp.route('/api/sale', methods=['POST'])
def add_sale():
    try:
        data = request.get_json()

        # Validation des données
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        magasin_id = data.get('magasin_id')
        quantity = data.get('quantite')
        montant = data.get('montant')

        if not user_id or not product_id or not magasin_id or not quantity or not montant:
            return jsonify({"message": "Tous les champs sont requis."}), 400
        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({"message": "La quantité doit être un entier positif."}), 400
        if not isinstance(montant, (int, float)) or montant < 0:
            return jsonify({"message": "Le montant doit être un nombre positif."}), 400

        # Vérifier si l'utilisateur, le produit et le magasin existent
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "L'utilisateur spécifié n'existe pas."}), 404

        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Le produit spécifié n'existe pas."}), 404

        magasin = Magasin.query.get(magasin_id)
        if not magasin:
            return jsonify({"message": "Le magasin spécifié n'existe pas."}), 404

        # Créer une nouvelle vente
        sale = Sales(user_id=user_id, product_id=product_id, magasin_id=magasin_id, quantite=quantity, montant=montant, date=datetime.utcnow())

        db.session.add(sale)
        db.session.commit()

        return jsonify({"message": "Sale added successfully"}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Erreur lors de l'ajout de la vente : {str(e)}"}), 500
    except Exception as e:
        return jsonify({"message": f"Erreur inattendue : {str(e)}"}), 500
