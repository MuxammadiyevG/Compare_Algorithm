from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

db = SQLAlchemy()

# Master key for encrypting sensitive data in database
DB_MASTER_KEY = os.environ.get('DB_MASTER_KEY', os.urandom(32))

# Initialize Argon2 password hasher with secure parameters
# Using Argon2id variant (hybrid of Argon2i and Argon2d)
ph = PasswordHasher(
    time_cost=3,        # Number of iterations
    memory_cost=65536,  # Memory usage in KiB (64 MB)
    parallelism=4,      # Number of parallel threads
    hash_len=32,        # Length of the hash in bytes
    salt_len=16         # Length of random salt in bytes
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    analysis_results = db.relationship('AnalysisResult', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash password using Argon2id"""
        self.password_hash = ph.hash(password)
    
    def check_password(self, password):
        """Verify password using Argon2id"""
        try:
            ph.verify(self.password_hash, password)
            
            # Check if hash needs rehashing (parameters changed)
            if ph.check_needs_rehash(self.password_hash):
                self.password_hash = ph.hash(password)
            
            return True
        except VerifyMismatchError:
            return False
    
    def __repr__(self):
        return f'<User {self.username}>'


class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)
    
    # Performance metrics
    encryption_time_ms = db.Column(db.Float)
    decryption_time_ms = db.Column(db.Float)
    total_time_ms = db.Column(db.Float)
    avg_cpu_percent = db.Column(db.Float)
    avg_memory_mb = db.Column(db.Float)
    
    # Security metrics
    entropy = db.Column(db.Float)
    key_size = db.Column(db.Integer)
    security_level = db.Column(db.String(20))
    
    # Scores
    t_performance = db.Column(db.Float)
    e_security = db.Column(db.Float)
    k_key_management = db.Column(db.Float)
    i_integrity = db.Column(db.Float)
    s_overall_score = db.Column(db.Float)
    
    # Data info
    plaintext_size = db.Column(db.Integer)
    ciphertext_size = db.Column(db.Integer)
    integrity_check = db.Column(db.Boolean)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalysisResult {self.algorithm} - Score: {self.s_overall_score}>'


class EncryptedData(db.Model):
    __tablename__ = 'encrypted_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    algorithm = db.Column(db.String(50), nullable=False)
    
    # Encrypted data (stored as base64)
    encrypted_content = db.Column(db.Text, nullable=False)
    key_id = db.Column(db.String(100), nullable=False)
    
    # Metadata
    original_filename = db.Column(db.String(255))
    content_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='encrypted_files')
    
    def set_encrypted_content(self, data):
        """Encrypt and store data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Encrypt with master key
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(DB_MASTER_KEY[:32]),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad data
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Store as base64 (IV + ciphertext)
        self.encrypted_content = base64.b64encode(iv + ciphertext).decode('utf-8')
    
    def get_decrypted_content(self):
        """Decrypt and return data"""
        # Decode from base64
        encrypted_data = base64.b64decode(self.encrypted_content)
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(DB_MASTER_KEY[:32]),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext
    
    def __repr__(self):
        return f'<EncryptedData {self.algorithm} - {self.original_filename}>'


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} at {self.timestamp}>'
