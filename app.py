# app.py
from flask import Flask
from config import Config
from models import db
from blueprints.products import products_bp
from blueprints.magasins import magasins_bp
from blueprints.users import users_bp
from blueprints.stock import stock_bp
from blueprints.sales import sales_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation de SQLAlchemy
db.init_app(app)

with app.app_context():
    db.create_all()  # Création des tables

# Enregistrement des blueprints
app.register_blueprint(products_bp)
app.register_blueprint(magasins_bp)
app.register_blueprint(users_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(sales_bp)

if __name__ == '__main__':
    app.run(debug=True)
