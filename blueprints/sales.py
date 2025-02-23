# blueprints/sales.py
from flask import Blueprint, request, jsonify
from models import Sales, db
from datetime import datetime

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/', methods=['GET'])
def get_sales():
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

@sales_bp.route('/<int:id>', methods=['GET'])
def get_sale(id):
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

@sales_bp.route('/<int:id>', methods=['PUT'])
def update_sale(id):
    s = Sales.query.get_or_404(id)
    data = request.get_json()
    s.user_id = data.get('user_id', s.user_id)
    s.product_id = data.get('product_id', s.product_id)
    s.magasin_id = data.get('magasin_id', s.magasin_id)
    s.quantite = data.get('quantite', s.quantite)
    s.montant = data.get('montant', s.montant)
    # Optionnel : mettre à jour la date si fournie
    # if data.get('date'):
    #     s.date = datetime.fromisoformat(data.get('date'))
    db.session.commit()
    return jsonify({'message': 'Sale updated successfully'})

@sales_bp.route('/<int:id>', methods=['DELETE'])
def delete_sale(id):
    s = Sales.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Sale deleted successfully'})
