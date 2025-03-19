from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from blueprints.products import products_bp
from blueprints.magasins import magasins_bp
from blueprints.users import users_bp
from waitress import serve
from blueprints.reception import reception_bp
from blueprints.sales import sales_bp
from blueprints.analyse import analyse_bp
from flask_jwt_extended import JWTManager
import os
import subprocess

app = Flask(__name__)
CORS(app)

# Configuration directe de la chaîne de connexion à la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/mybussiness'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de JWT
app.config['JWT_SECRET_KEY'] = 'votre_clé_secrète'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 heure

# Initialisation de SQLAlchemy
db.init_app(app)

# Initialisation de Migrate
migrate = Migrate(app, db)

# Initialisation de JWT
jwt = JWTManager(app)


# Enregistrement des blueprints
app.register_blueprint(products_bp)
app.register_blueprint(magasins_bp)
app.register_blueprint(users_bp)
app.register_blueprint(reception_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(analyse_bp)

if __name__ == '__main__':
    print("Démarrage du serveur Flask...")
    serve(app, host='127.0.0.1', port=5000)
