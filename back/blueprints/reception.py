from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models import Reception, ReceptionItem, Magasin, Product, Stock, db

reception_bp = Blueprint('reception', __name__, url_prefix='/reception')

@reception_bp.route('/', methods=['GET'])
def get_receptions():
    try:
        receptions = Reception.query.all()
        return jsonify([{
            'id': r.id,
            'magasin_id': r.magasin_id,
            'supplier': r.supplier,
            'total': r.total_montant,
            'date': r.date_reception.strftime('%d/%m/%Y')  # Convert date to year/month/day format
        } for r in receptions])
    
    except SQLAlchemyError as e:
        return jsonify({'message': 'Une erreur est survenue lors de la récupération des réceptions.', 'error': str(e)}), 500

@reception_bp.route('/add', methods=['POST'])
def add_reception():
    try:
        data = request.get_json()
        
        # Récupération des données générales de la réception
        magasin_id = data.get('magasin')
        fournisseur = data.get('fournisseur')
        produits = data.get('produits', [])  # Liste des produits reçus
        total = data.get('total', 0)

        print(data)
        # Création de la réception
        reception = Reception(
            magasin_id=magasin_id,
            supplier=fournisseur,
            total_montant = total,
            date_reception=datetime.utcnow(),
        )
        print(reception)

        db.session.add(reception)
        print(reception)
        db.session.flush()  # Permet d'obtenir l'ID de la réception avant le commit
        print(reception)

        print(reception.id)
        total_reception = 0

        # Ajout des produits reçus
        for produit in produits:
            print(produit)
            product_id = produit.get('id')
            quantite = produit.get('quantity', 0)
            quantite_cartons = produit.get('quantite_cartons', 1)  # Par défaut, 1 carton si non fourni
            prix_unitaire = produit.get('prix_unitaire', 0)


            montant_total = float(quantite * prix_unitaire)
            item = ReceptionItem(
                reception_id=reception.id,
                product_id=product_id,
                quantite=quantite,
                prix_unitaire=prix_unitaire,
                montant_total=montant_total
            )

            print(item)

            total_reception = total + montant_total  # Calcul du total de la réception

            # Met à jour le stock dans le magasin correspondant
            stock = Stock.query.filter_by(product_id=product_id, magasin_id=magasin_id).first()
            if stock:
                stock.quantite += (quantite * quantite_cartons)
            else:
                stock = Stock(
                    product_id=product_id,
                    magasin_id=magasin_id,
                    quantite=quantite * quantite_cartons
                )
                db.session.add(stock)

            db.session.add(item)

        # Mettre à jour le total de la réception
        reception.total = total_reception

        # Commit toutes les modifications
        db.session.commit()

        return jsonify({'message': 'Réception enregistrée avec succès', 'reception_id': reception.id}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Une erreur est survenue lors de l\'ajout de la réception.', 'error': str(e)}), 500
