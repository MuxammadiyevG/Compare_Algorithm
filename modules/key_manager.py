import os
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import logging

class KeyManager:
    def __init__(self, vault_path, audit_log_path):
        """
        Initialize Key Manager with vault path and audit log
        """
        self.vault_path = vault_path
        self.audit_log_path = audit_log_path
        self.master_key = self._get_or_create_master_key()
        self.keys = {}
        self._load_keys()
        
        # Setup logging
        logging.basicConfig(
            filename=audit_log_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def _get_or_create_master_key(self):
        """Get or create master key for encrypting the key vault"""
        master_key_file = os.path.join(os.path.dirname(self.vault_path), '.master_key')
        
        if os.path.exists(master_key_file):
            with open(master_key_file, 'rb') as f:
                return f.read()
        else:
            master_key = os.urandom(32)  # 256-bit key
            os.makedirs(os.path.dirname(master_key_file), exist_ok=True)
            with open(master_key_file, 'wb') as f:
                f.write(master_key)
            return master_key
    
    def _encrypt_vault(self, data):
        """Encrypt vault data using master key"""
        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad data
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode('utf-8')) + padder.finalize()
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Return IV + ciphertext
        return iv + ciphertext
    
    def _decrypt_vault(self, encrypted_data):
        """Decrypt vault data using master key"""
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')
    
    def _load_keys(self):
        """Load keys from encrypted vault"""
        if os.path.exists(self.vault_path):
            try:
                with open(self.vault_path, 'rb') as f:
                    encrypted_data = f.read()
                
                if encrypted_data:
                    decrypted_data = self._decrypt_vault(encrypted_data)
                    self.keys = json.loads(decrypted_data)
                    
                    # Convert base64 strings back to bytes
                    for key_id, key_data in self.keys.items():
                        key_data['key'] = base64.b64decode(key_data['key'])
                        key_data['iv_or_nonce'] = base64.b64decode(key_data['iv_or_nonce'])
            except Exception as e:
                logging.error(f"Error loading keys: {str(e)}")
                self.keys = {}
    
    def _save_keys(self):
        """Save keys to encrypted vault"""
        # Convert bytes to base64 for JSON serialization
        serializable_keys = {}
        for key_id, key_data in self.keys.items():
            serializable_keys[key_id] = {
                'key': base64.b64encode(key_data['key']).decode('utf-8'),
                'iv_or_nonce': base64.b64encode(key_data['iv_or_nonce']).decode('utf-8'),
                'algorithm': key_data['algorithm'],
                'created_at': key_data['created_at'],
                'user': key_data['user']
            }
        
        # Encrypt and save
        json_data = json.dumps(serializable_keys)
        encrypted_data = self._encrypt_vault(json_data)
        
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
        with open(self.vault_path, 'wb') as f:
            f.write(encrypted_data)
    
    def create_key(self, algorithm, user='system'):
        """
        Create and store a new encryption key
        Returns: key_id
        """
        key_id = f"{algorithm}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Generate key based on algorithm
        if algorithm == 'AES':
            key = os.urandom(32)  # 256-bit
            iv_or_nonce = os.urandom(16)
        elif algorithm == 'DES':
            key = os.urandom(8)
            iv_or_nonce = os.urandom(8)
        elif algorithm == 'Blowfish':
            key = os.urandom(16)  # 128-bit
            iv_or_nonce = os.urandom(8)
        elif algorithm == 'ChaCha20':
            key = os.urandom(32)  # 256-bit
            iv_or_nonce = os.urandom(16)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        # Store key
        self.keys[key_id] = {
            'key': key,
            'iv_or_nonce': iv_or_nonce,
            'algorithm': algorithm,
            'created_at': datetime.now().isoformat(),
            'user': user
        }
        
        self._save_keys()
        
        # Audit log
        logging.info(f"Key created - ID: {key_id}, Algorithm: {algorithm}, User: {user}")
        
        return key_id
    
    def get_key(self, key_id):
        """
        Retrieve a key by ID
        Returns: (key, iv_or_nonce, algorithm)
        """
        if key_id not in self.keys:
            raise ValueError(f"Key not found: {key_id}")
        
        key_data = self.keys[key_id]
        
        # Audit log
        logging.info(f"Key accessed - ID: {key_id}, Algorithm: {key_data['algorithm']}")
        
        return key_data['key'], key_data['iv_or_nonce'], key_data['algorithm']
    
    def rotate_key(self, old_key_id, user='system'):
        """
        Rotate a key (create new key with same algorithm)
        Returns: new_key_id
        """
        if old_key_id not in self.keys:
            raise ValueError(f"Key not found: {old_key_id}")
        
        algorithm = self.keys[old_key_id]['algorithm']
        new_key_id = self.create_key(algorithm, user)
        
        # Audit log
        logging.info(f"Key rotated - Old ID: {old_key_id}, New ID: {new_key_id}, User: {user}")
        
        return new_key_id
    
    def delete_key(self, key_id, user='system'):
        """Delete a key"""
        if key_id not in self.keys:
            raise ValueError(f"Key not found: {key_id}")
        
        algorithm = self.keys[key_id]['algorithm']
        del self.keys[key_id]
        self._save_keys()
        
        # Audit log
        logging.info(f"Key deleted - ID: {key_id}, Algorithm: {algorithm}, User: {user}")
    
    def list_keys(self):
        """List all keys (without exposing actual key values)"""
        return {
            key_id: {
                'algorithm': key_data['algorithm'],
                'created_at': key_data['created_at'],
                'user': key_data['user']
            }
            for key_id, key_data in self.keys.items()
        }
    
    def get_audit_logs(self, limit=100):
        """Get recent audit logs"""
        if not os.path.exists(self.audit_log_path):
            return []
        
        with open(self.audit_log_path, 'r') as f:
            lines = f.readlines()
        
        return lines[-limit:]
