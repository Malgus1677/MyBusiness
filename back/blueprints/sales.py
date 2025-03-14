from flask import Blueprint, request, jsonify
from models import Sales, Product, User, Magasin, SaleItem, Stock, db
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

@sales_bp.route('/add', methods=['POST'])
def add_sale():
    try:
        data = request.get_json()
        print(data)
        
        # Vérifier les données requises
        if 'magasin_id' not in data or 'products' not in data or 'totalPrice' not in data:
            return jsonify({'message': 'Données manquantes'}), 400

        # Créer une nouvelle vente
        new_sale = Sales(
            magasin_id=data['magasin_id'],
            total=data['totalPrice'],
            user_id=data.get('user_id', None),
            payment_method=data['paymentMethod'],
            montant_donne=data.get('montantDonne', 0),
            somme_rendue=data.get('sommeRendue', 0)
        )
        
        db.session.add(new_sale)
        db.session.flush()  # Permet de récupérer l'ID avant commit

        # Ajouter les articles associés
        for item in data['products']:
            product = Product.query.get(item['id'])
            if not product:
                return jsonify({'message': f'Produit {item["id"]} introuvable'}), 404

            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=item['id'],
                quantite=item['quantity'],
                montant=item['totalPrice']
            )
            db.session.add(sale_item)

            stock = Stock.query.filter_by(product_id=item['id'], magasin_id=data['magasin_id']).first()
            if not stock:
                return jsonify({'message': 'Stock introuvable'}), 404

            # Mettre à jour le stock
            stock.quantite -= item['quantity']
            db.session.add(stock)

        db.session.commit()
        return jsonify({'message': 'Vente enregistrée avec succès', 'sale_id': new_sale.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Erreur lors de l\'enregistrement', 'error': str(e)}), 500
