# config.py
import os

class Config:
    # Exemple de chaîne de connexion pour MySQL avec PyMySQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/mybussiness')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
