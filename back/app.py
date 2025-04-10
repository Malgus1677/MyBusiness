import os
import logging
from waitress import serve
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
from blueprints.users import users_bp
from blueprints.magasins import magasins_bp
from blueprints.products import products_bp
from blueprints.reception import reception_bp
from blueprints.sales import sales_bp
from blueprints.analyse import analyse_bp
from models import db
from flask_jwt_extended import JWTManager

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configurer les logs
logging.basicConfig(
    level=logging.INFO,  # Niveau de log
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format du log
    handlers=[
        logging.FileHandler('/var/log/mybusiness.out.log'),  # Log dans un fichier
        logging.StreamHandler()  # Log dans la console
    ]
)
# Afficher les variables d'environnement pour vérifier
logging.info("DB_USER: %s", os.getenv('DB_USER'))
logging.info("DB_HOST: %s", os.getenv('DB_HOST'))
logging.info("DB_NAME: %s", os.getenv('DB_NAME'))
logging.info("DB_PASSWORD: %s", os.getenv('DB_PASSWORD'))

# Créer l'application Flask
app = Flask(__name__)

# Configuration de la chaîne de connexion à la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Initialiser SQLAlchemy avec init_app
db.init_app(app)

# Initialiser JWTManager
jwt = JWTManager(app)

# Test de la connexion à la base de données
with app.app_context():  # Utilisation du contexte d'application
    try:
        connection = db.engine.connect()  # Tentative de connexion à la base de données
        connection.close()
        logging.info("Connexion à la base de données réussie.")
    except OperationalError as e:
        logging.error("Erreur de connexion à la base de données: %s", e)
        raise Exception("Erreur de connexion à la base de données.")

# Enregistrer le Blueprint
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(magasins_bp, url_prefix='/magasins')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(reception_bp, url_prefix='/reception')
app.register_blueprint(sales_bp, url_prefix='/sales')
app.register_blueprint(analyse_bp, url_prefix='/analyse')



# Démarrage de l'application
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
