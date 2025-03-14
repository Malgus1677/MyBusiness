from flask import Blueprint, jsonify
from models import db, Sales, SaleItem, Reception, ReceptionItem, Stock, Product, Magasin, User
from sqlalchemy import func, desc
from datetime import datetime, timedelta

analyse_bp = Blueprint('analyse', __name__, url_prefix='/analyse')

@analyse_bp.route('/', methods=['GET'])
def analyse_magasin():
    try:
        # Chiffre d'affaires total
        total_revenue = db.session.query(func.sum(Sales.total)).scalar() or 0
        
        # Bénéfices (ventes - coûts d'achat)
        total_cost = db.session.query(func.sum(ReceptionItem.montant_total)).scalar() or 0
        total_profit = total_revenue - total_cost
        
        # Nombre de ventes
        total_sales = Sales.query.count()
        
        # Nombre de réceptions
        total_receptions = Reception.query.count()
        
        # Top 5 produits les plus vendus
        top_products = (
            db.session.query(Product.nom, func.sum(SaleItem.quantite).label("total_vendu"))
            .join(SaleItem, Product.id == SaleItem.product_id)
            .group_by(Product.id)
            .order_by(desc("total_vendu"))
            .limit(5)
            .all()
        )
        
        # Valeur du stock actuel
        stock_value = (
            db.session.query(func.sum(Stock.quantite * Product.prix)).join(Product).scalar() or 0
        )
        
        # Performances des magasins
        magasins_performance = (
            db.session.query(Magasin.nom, func.sum(Sales.total).label("chiffre_affaires"))
            .join(Sales, Magasin.id == Sales.magasin_id)
            .group_by(Magasin.id)
            .order_by(desc("chiffre_affaires"))
            .all()
        )
        
        # Employés ayant réalisé le plus de ventes
        best_employees = (
            db.session.query(User.nom, User.prenom, func.count(Sales.id).label("ventes_realisees"))
            .join(Sales, User.id == Sales.user_id)
            .group_by(User.id)
            .order_by(desc("ventes_realisees"))
            .limit(5)
            .all()
        )
        
        # Tendances des ventes des 7 derniers jours
        last_7_days = datetime.now() - timedelta(days=7)
        daily_sales = (
            db.session.query(func.date(Sales.date), func.sum(Sales.total))
            .filter(Sales.date >= last_7_days)
            .group_by(func.date(Sales.date))
            .order_by(func.date(Sales.date))
            .all()
        )

        # Ventes par jour de la semaine
        sales_by_weekday = (
            db.session.query(func.date_format(Sales.date, '%w').label('weekday'), func.sum(Sales.total))
            .group_by('weekday')
            .order_by('weekday')
            .all()
        )

        # Ventes par mois
        sales_by_month = (
            db.session.query(func.date_format(Sales.date, '%Y-%m').label('month'), func.sum(Sales.total))
            .group_by('month')
            .order_by('month')
            .all()
        )

        # Calcul de la rotation des stocks par mois
        stock_turnover_by_month = []
        for month, total_sales in sales_by_month:
            # Calcul du CAMV pour le mois
            camv_query = (
                db.session.query(func.sum(SaleItem.quantite * Product.prix_d_achat))
                .join(SaleItem, SaleItem.sale_id == Sales.id)
                .join(Product, Product.id == SaleItem.product_id)
                .filter(func.date_format(Sales.date, '%Y-%m') == month)
                .scalar() or 0
            )
            print(camv_query)

            
            # Calcul de la rotation des stocks
           

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
               
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
