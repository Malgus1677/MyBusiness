# blueprints/stock.py
from flask import Blueprint, request, jsonify
from models import Stock, db

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
