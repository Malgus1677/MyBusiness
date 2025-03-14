from flask import Blueprint, jsonify
from models import db, Sales, SaleItem, Reception, ReceptionItem, Stock, Product, Magasin, User
from sqlalchemy import func, desc
from datetime import datetime, timedelta

analyse_bp = Blueprint('analyse', __name__, url_prefix='/analyse')

@analyse_bp.route('/magasin/<int:magasin_id>', methods=['GET'])
def analyse_magasin(magasin_id):
    try:
        # Chiffre d'affaires total pour le magasin
        total_revenue = db.session.query(func.sum(Sales.total)) \
            .filter(Sales.magasin_id == magasin_id) \
            .scalar() or 0
        
        # Bénéfices (ventes - coûts d'achat)
        # On récupère le coût total des réceptions via la table Reception (qui possède la clé magasin_id)
        total_cost = db.session.query(func.sum(Reception.total_montant)) \
            .filter(Reception.magasin_id == magasin_id) \
            .scalar() or 0
        total_profit = total_revenue - total_cost
        
        # Nombre de ventes pour le magasin
        total_sales = db.session.query(Sales) \
            .filter(Sales.magasin_id == magasin_id) \
            .count()
        
        # Valeur totale des réceptions (somme des montants) pour le magasin
        total_receptions = db.session.query(func.sum(Reception.total_montant)) \
            .filter(Reception.magasin_id == magasin_id) \
            .scalar() or 0
        
        # Top 5 produits les plus vendus pour le magasin
        top_products = (
            db.session.query(Product.nom, func.sum(SaleItem.quantite).label("total_vendu"))
            .join(SaleItem, SaleItem.product_id == Product.id)
            .join(Sales, Sales.id == SaleItem.sale_id)
            .filter(Sales.magasin_id == magasin_id)
            .group_by(Product.id)
            .order_by(desc("total_vendu"))
            .limit(5)
            .all()
        )
        
        # Valeur du stock actuel pour le magasin
        stock_value = (
            db.session.query(func.sum(Stock.quantite * Product.prix))
            .join(Product, Product.id == Stock.product_id)
            .filter(Stock.magasin_id == magasin_id)
            .scalar() or 0
        )
        
        # Performances des magasins (liste de tous les magasins avec leur chiffre d'affaires)
        magasins_performance = (
            db.session.query(Magasin.nom, func.sum(Sales.total).label("chiffre_affaires"))
            .join(Sales, Sales.magasin_id == Magasin.id)
            .group_by(Magasin.id)
            .order_by(desc("chiffre_affaires"))
            .all()
        )
        
        # Employés ayant réalisé le plus de ventes dans ce magasin
        best_employees = (
            db.session.query(User.nom, User.prenom, func.count(Sales.id).label("ventes_realisees"))
            .join(Sales, Sales.user_id == User.id)
            .filter(Sales.magasin_id == magasin_id)
            .group_by(User.id)
            .order_by(desc("ventes_realisees"))
            .limit(5)
            .all()
        )
        
        # Tendances des ventes des 7 derniers jours pour le magasin
        last_7_days = datetime.now() - timedelta(days=7)
        daily_sales = (
            db.session.query(func.date(Sales.date), func.sum(Sales.total))
            .filter(Sales.date >= last_7_days, Sales.magasin_id == magasin_id)
            .group_by(func.date(Sales.date))
            .order_by(func.date(Sales.date))
            .all()
        )

        # Ventes par jour de la semaine pour le magasin
        sales_by_weekday = (
            db.session.query(func.date_format(Sales.date, '%w').label('weekday'), func.sum(Sales.total))
            .filter(Sales.magasin_id == magasin_id)
            .group_by('weekday')
            .order_by('weekday')
            .all()
        )

        # Ventes par mois pour le magasin
        sales_by_month = (
            db.session.query(func.date_format(Sales.date, '%Y-%m').label('month'), func.sum(Sales.total))
            .filter(Sales.magasin_id == magasin_id)
            .group_by('month')
            .order_by('month')
            .all()
        )

        # Indicateurs Complémentaires

        # Panier moyen : montant moyen dépensé par vente
        panier_moyen = total_revenue / total_sales if total_sales > 0 else 0

        # Coût des marchandises vendues (CAMV) : on suppose que Product.prix représente le coût d'achat
        camv = db.session.query(
            func.sum(SaleItem.quantite * Product.prix)
        ).join(Sales, Sales.id == SaleItem.sale_id) \
         .filter(Sales.magasin_id == magasin_id) \
         .scalar() or 0

        # Valeur moyenne du stock pour le magasin
        avg_stock_value = db.session.query(
            func.avg(Stock.quantite * Product.prix)
        ).join(Product, Product.id == Stock.product_id) \
         .filter(Stock.magasin_id == magasin_id) \
         .scalar() or 0

        # Rotation des stocks : CAMV / Valeur moyenne du stock
        rotation_des_stocks = camv / avg_stock_value if avg_stock_value > 0 else 0

        # Délai moyen de stockage : (Valeur moyenne du stock / CAMV) * 365 jours
        delai_moyen_stockage = (avg_stock_value / camv) * 365 if camv > 0 else 0

        # Marge bénéficiaire en pourcentage : (Bénéfice / Chiffre d'affaires) * 100
        marge_beneficiaire = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0

        # Résultats de l'analyse
        result = {
            "total_revenue": round(total_revenue, 2),
            "total_profit": round(total_profit, 2),
            "total_sales": round(total_sales, 2),
            "total_receptions": round(total_receptions, 2),
            "top_products": [{"nom": p[0], "quantite_vendue": round(p[1], 2)} for p in top_products],
            "stock_value": round(stock_value, 2),
            "magasins_performance": [{"nom": m[0], "chiffre_affaires": round(m[1], 2)} for m in magasins_performance],
            "best_employees": [{"nom": e[0], "prenom": e[1], "ventes": round(e[2], 2)} for e in best_employees],
            "daily_sales": [{"date": str(d[0]), "total": round(d[1], 2)} for d in daily_sales],
            "period_analysis": {
                "sales_by_weekday": [{"weekday": d[0], "total": round(d[1], 2)} for d in sales_by_weekday],
                "sales_by_month": [{"month": d[0], "total": round(d[1], 2)} for d in sales_by_month],
            },
            "additional_indicators": {
                "panier_moyen": round(panier_moyen, 2),
                "rotation_des_stocks": round(rotation_des_stocks, 2),
                "delai_moyen_stockage": round(delai_moyen_stockage, 2),
                "marge_beneficiaire": round(marge_beneficiaire, 2)
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
