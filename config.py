import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Master encryption key for key wrapping
    MASTER_KEY = os.environ.get('MASTER_KEY')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///encryption_audit.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # Temporary encrypted files folder
    TEMP_ENCRYPTED_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_encrypted')
    
    # Key vault configuration
    KEY_VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'key_vault.enc')
    
    # Audit log configuration
    AUDIT_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'audit.log')
    
    # Analysis weights
    WEIGHT_PERFORMANCE = 0.25
    WEIGHT_SECURITY = 0.35
    WEIGHT_KEY_MANAGEMENT = 0.25
    WEIGHT_INTEGRITY = 0.15
