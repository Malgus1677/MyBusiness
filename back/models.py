# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Magasin(db.Model):
    __tablename__ = 'magasins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # ex. 'admin', 'manager', 'employe'
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=True)
    magasin = db.relationship('Magasin', backref='users')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    # Prix d'achat du produit
    prix = db.Column(db.Float, nullable=False)
    # Nombre d'unités par carton (ex. 12 unités par carton)
    unites_par_carton = db.Column(db.Integer, nullable=False, default=1)
    prix_de_vente =db.Column(db.Float, nullable=False, default=1)
    prix_unitaire = db.Column(db.Float, nullable=False, default=1)
    
   
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=False)
    # Quantité exprimée en unités
    quantite = db.Column(db.Integer, nullable=False, default=0)
    product = db.relationship('Product', backref='stock_items')
    magasin = db.relationship('Magasin', backref='stock_items')

class Reception(db.Model):
    __tablename__ = 'receptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=False)
    supplier = db.Column(db.String(100), nullable=False)
    date_reception = db.Column(db.DateTime, default=datetime.now)
    total_montant = db.Column(db.Float, nullable=False, default=0)  # Somme totale de la réception
    magasin = db.relationship('Magasin', backref='receptions')
    items = db.relationship('ReceptionItem', backref='reception', lazy=True, cascade="all, delete-orphan")


class ReceptionItem(db.Model):
    __tablename__ = 'reception_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reception_id = db.Column(db.Integer, db.ForeignKey('receptions.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)  # Quantité reçue
    prix_unitaire = db.Column(db.Float, nullable=False)  # Prix unitaire du produit
    montant_total = db.Column(db.Float, nullable=False)  # Prix total pour cet article (quantite * prix_unitaire)

    product = db.relationship('Product', backref='reception_items')

class Sales(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    magasin_id = db.Column(db.Integer, db.ForeignKey('magasins.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Facultatif si non utilisé
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # 'Carte bancaire' ou 'Espèces'
    montant_donne = db.Column(db.Float, nullable=False, default=0)  # Argent donné par le client
    somme_rendue = db.Column(db.Float, nullable=False, default=0)  # Monnaie rendue au client
    date = db.Column(db.DateTime, default=datetime.now)

    magasin = db.relationship('Magasin', backref='sales')
    user = db.relationship('User', backref='sales')
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade="all, delete-orphan")


class SaleItem(db.Model):
    __tablename__ = 'sale_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)  # Nombre d'unités vendues
    montant = db.Column(db.Float, nullable=False)  # Prix total (quantité * prix unitaire)

    product = db.relationship('Product', backref='sale_items')
    sale = db.relationship('Sales', backref='sale_items')
