import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Use MYSQL_DATABASE_URL if set, otherwise fall back to a default local MySQL connection string or SQLite
    # NOTE: To use MySQL, set DATABASE_URL in .env like: 
    # DATABASE_URL=mysql+pymysql://username:password@localhost/smartcampus
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///smartcampus.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
