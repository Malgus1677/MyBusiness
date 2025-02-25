# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Magasin(db.Model):
    __tablename__ = 'magasins'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # ex. 'admin', 'manager', 'employe'
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=True)
    magasin = db.relationship('Magasin', backref='users')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    # Prix d'achat du produit
    prix = db.Column(db.Float, nullable=False)
    # Nombre d'unités par carton (ex. 12 unités par carton)
    unites_par_carton = db.Column(db.Integer, nullable=False, default=1)
    prix_de_vente =db.Column(db.Integer, nullable=False, default=1)
    prix_unitaire = db.Column(db.Float, nullable=False, default=1)
    
   
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=False)
    # Quantité exprimée en unités
    quantite = db.Column(db.Integer, nullable=False, default=0)
    product = db.relationship('Product', backref='stock_items')
    magasin = db.relationship('Magasin', backref='stock_items')

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)  # en unités
    montant = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='sales')
    product = db.relationship('Product', backref='sales')
    magasin = db.relationship('Magasin', backref='sales')
