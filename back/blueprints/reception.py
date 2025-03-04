from flask import Blueprint, request, jsonify
from models import Reception, Product, Stock, db

reception_bp = Blueprint('reception', __name__, url_prefix='/reception')

@reception_bp.route('/add', methods=['POST'])
def create_reception():
    data = request.get_json()
    print(data)
    magasin = data.get('magasin')
    supplier = data.get('fournisseur')
    total = data.get('total')
    products = data.get('produits')

    # Traiter chaque produit
    for product in products:
        print(product)
        product_id = product.get('id')
        quantite = product.get('quantity')
        prix = product.get('prix')
        quantite_cartons = product.get('quantite_cartons')

        reception = Reception(
            product_id=product_id,
            supplier=supplier,
            magasin_id=magasin,
            quantite=quantite,
            montant=total,
        )

        # Mise à jour du stock
        stock = Stock.query.filter_by(product_id=product_id, magasin_id=magasin).first()
        if stock:
            stock.quantite += quantite
        else:
            stock = Stock(
                product_id=product_id,
                magasin_id=magasin,
                quantite=quantite * quantite_cartons
            )
            db.session.add(stock)
        
        db.session.add(reception)
    
    # Commit une fois pour tous les produits
    db.session.commit()
    return jsonify({'message': 'Réception créée avec succès'}), 201
