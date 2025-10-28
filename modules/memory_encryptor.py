"""
In-Memory File Encryption Module
Handles encryption/decryption without storing files on disk
Uses MASTER_KEY for key wrapping
"""

import os
import base64
from io import BytesIO
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.fernet import Fernet


class MemoryEncryptor:
    """
    Handles in-memory file encryption with key wrapping
    """
    
    def __init__(self, master_key_b64):
        """
        Initialize with MASTER_KEY from environment
        
        Args:
            master_key_b64: Base64 encoded 256-bit master key
        """
        self.master_key = base64.b64decode(master_key_b64)
        if len(self.master_key) != 32:
            raise ValueError("MASTER_KEY must be 32 bytes (256 bits)")
    
    def encrypt_file_aes(self, file_stream):
        """
        Encrypt file using AES-256-CBC with random session key
        
        Args:
            file_stream: BytesIO or file-like object
            
        Returns:
            tuple: (encrypted_data_stream, encrypted_key_stream)
        """
        # Read file data into memory
        file_data = file_stream.read()
        
        # Generate random session key (32 bytes for AES-256)
        session_key = os.urandom(32)
        iv = os.urandom(16)  # AES block size
        
        # Encrypt file data with session key
        cipher = Cipher(
            algorithms.AES(session_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad data
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV + ciphertext
        encrypted_data = iv + ciphertext
        
        # Wrap session key with MASTER_KEY
        wrapped_key = self._wrap_key(session_key)
        
        # Return as BytesIO streams
        encrypted_data_stream = BytesIO(encrypted_data)
        encrypted_key_stream = BytesIO(wrapped_key)
        
        return encrypted_data_stream, encrypted_key_stream
    
    def decrypt_file_aes(self, encrypted_data_stream, encrypted_key_stream):
        """
        Decrypt file using AES-256-CBC
        
        Args:
            encrypted_data_stream: BytesIO with encrypted file data
            encrypted_key_stream: BytesIO with wrapped session key
            
        Returns:
            BytesIO: Decrypted file data
        """
        # Read encrypted data
        encrypted_data = encrypted_data_stream.read()
        wrapped_key = encrypted_key_stream.read()
        
        # Unwrap session key
        session_key = self._unwrap_key(wrapped_key)
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Decrypt
        cipher = Cipher(
            algorithms.AES(session_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        # Return as BytesIO stream
        return BytesIO(plaintext)
    
    def encrypt_file_fernet(self, file_stream):
        """
        Encrypt file using Fernet (AES-128-CBC + HMAC) with random session key
        
        Args:
            file_stream: BytesIO or file-like object
            
        Returns:
            tuple: (encrypted_data_stream, encrypted_key_stream)
        """
        # Read file data into memory
        file_data = file_stream.read()
        
        # Generate random Fernet key (32 bytes base64 encoded)
        session_key = Fernet.generate_key()
        fernet = Fernet(session_key)
        
        # Encrypt file data
        ciphertext = fernet.encrypt(file_data)
        
        # Wrap session key with MASTER_KEY
        wrapped_key = self._wrap_key(session_key)
        
        # Return as BytesIO streams
        encrypted_data_stream = BytesIO(ciphertext)
        encrypted_key_stream = BytesIO(wrapped_key)
        
        return encrypted_data_stream, encrypted_key_stream
    
    def decrypt_file_fernet(self, encrypted_data_stream, encrypted_key_stream):
        """
        Decrypt file using Fernet
        
        Args:
            encrypted_data_stream: BytesIO with encrypted file data
            encrypted_key_stream: BytesIO with wrapped session key
            
        Returns:
            BytesIO: Decrypted file data
        """
        # Read encrypted data
        ciphertext = encrypted_data_stream.read()
        wrapped_key = encrypted_key_stream.read()
        
        # Unwrap session key
        session_key = self._unwrap_key(wrapped_key)
        
        # Decrypt
        fernet = Fernet(session_key)
        plaintext = fernet.decrypt(ciphertext)
        
        # Return as BytesIO stream
        return BytesIO(plaintext)
    
    def encrypt_file_chacha20(self, file_stream):
        """
        Encrypt file using ChaCha20 with random session key
        
        Args:
            file_stream: BytesIO or file-like object
            
        Returns:
            tuple: (encrypted_data_stream, encrypted_key_stream)
        """
        # Read file data into memory
        file_data = file_stream.read()
        
        # Generate random session key (32 bytes for ChaCha20)
        session_key = os.urandom(32)
        nonce = os.urandom(16)  # ChaCha20 nonce
        
        # Encrypt file data with session key
        cipher = Cipher(
            algorithms.ChaCha20(session_key, nonce),
            mode=None,
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(file_data) + encryptor.finalize()
        
        # Combine nonce + ciphertext
        encrypted_data = nonce + ciphertext
        
        # Wrap session key with MASTER_KEY
        wrapped_key = self._wrap_key(session_key)
        
        # Return as BytesIO streams
        encrypted_data_stream = BytesIO(encrypted_data)
        encrypted_key_stream = BytesIO(wrapped_key)
        
        return encrypted_data_stream, encrypted_key_stream
    
    def decrypt_file_chacha20(self, encrypted_data_stream, encrypted_key_stream):
        """
        Decrypt file using ChaCha20
        
        Args:
            encrypted_data_stream: BytesIO with encrypted file data
            encrypted_key_stream: BytesIO with wrapped session key
            
        Returns:
            BytesIO: Decrypted file data
        """
        # Read encrypted data
        encrypted_data = encrypted_data_stream.read()
        wrapped_key = encrypted_key_stream.read()
        
        # Unwrap session key
        session_key = self._unwrap_key(wrapped_key)
        
        # Extract nonce and ciphertext
        nonce = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Decrypt
        cipher = Cipher(
            algorithms.ChaCha20(session_key, nonce),
            mode=None,
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Return as BytesIO stream
        return BytesIO(plaintext)
    
    def _wrap_key(self, session_key):
        """
        Wrap (encrypt) session key with MASTER_KEY using AES-256-ECB
        
        Args:
            session_key: bytes to wrap
            
        Returns:
            bytes: Wrapped key
        """
        # Use AES-ECB for key wrapping (simple and secure for small data)
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.ECB(),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad session key if needed
        padder = padding.PKCS7(128).padder()
        padded_key = padder.update(session_key) + padder.finalize()
        
        # Encrypt
        wrapped = encryptor.update(padded_key) + encryptor.finalize()
        
        return wrapped
    
    def _unwrap_key(self, wrapped_key):
        """
        Unwrap (decrypt) session key with MASTER_KEY
        
        Args:
            wrapped_key: bytes to unwrap
            
        Returns:
            bytes: Original session key
        """
        # Decrypt with MASTER_KEY
        cipher = Cipher(
            algorithms.AES(self.master_key),
            modes.ECB(),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_key = decryptor.update(wrapped_key) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(128).unpadder()
        session_key = unpadder.update(padded_key) + unpadder.finalize()
        
        return session_key
