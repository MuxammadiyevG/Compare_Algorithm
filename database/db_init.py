import sys
import os

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import db, User, AnalysisResult, EncryptedData, AuditLog
from flask import Flask
from config import Config

def init_db():
    """Initialize database and create tables"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Default admin user created (username: admin, password: admin123)")
        
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(Config.KEY_VAULT_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(Config.AUDIT_LOG_PATH), exist_ok=True)
        
        print("[OK] Database initialized successfully!")
        print(f"[OK] Database location: {Config.SQLALCHEMY_DATABASE_URI}")

if __name__ == '__main__':
    init_db()
