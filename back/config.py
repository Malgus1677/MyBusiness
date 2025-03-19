from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/mybussiness')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
