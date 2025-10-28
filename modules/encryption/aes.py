import time
import tracemalloc
import psutil
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import math

class AESEncryption:
    def __init__(self, key_size=256):
        """
        Initialize AES encryption with specified key size (128, 192, or 256 bits)
        """
        self.key_size = key_size
        self.key = None
        self.iv = None
        
    def generate_key(self):
        """Generate a random AES key"""
        self.key = os.urandom(self.key_size // 8)
        self.iv = os.urandom(16)  # AES block size is always 16 bytes
        return self.key, self.iv
    
    def set_key(self, key, iv):
        """Set existing key and IV"""
        self.key = key
        self.iv = iv
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using AES-CBC
        Returns: (ciphertext, encryption_time_ms, cpu_percent, memory_mb, entropy)
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # Start performance monitoring
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=0.1)
        tracemalloc.start()
        start_time = time.time()
        
        # Padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # Encryption
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(self.iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # End performance monitoring
        end_time = time.time()
        cpu_after = process.cpu_percent(interval=0.1)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        encryption_time = (end_time - start_time) * 1000  # Convert to ms
        cpu_usage = (cpu_before + cpu_after) / 2
        memory_usage = peak / (1024 * 1024)  # Convert to MB
        entropy = self._calculate_entropy(ciphertext)
        
        return ciphertext, encryption_time, cpu_usage, memory_usage, entropy
    
    def decrypt(self, ciphertext):
        """
        Decrypt ciphertext using AES-CBC
        Returns: (plaintext, decryption_time_ms, cpu_percent, memory_mb)
        """
        # Start performance monitoring
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=0.1)
        tracemalloc.start()
        start_time = time.time()
        
        # Decryption
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(self.iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Unpadding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        # End performance monitoring
        end_time = time.time()
        cpu_after = process.cpu_percent(interval=0.1)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        decryption_time = (end_time - start_time) * 1000  # Convert to ms
        cpu_usage = (cpu_before + cpu_after) / 2
        memory_usage = peak / (1024 * 1024)  # Convert to MB
        
        return plaintext, decryption_time, cpu_usage, memory_usage
    
    def _calculate_entropy(self, data):
        """Calculate Shannon entropy of data"""
        if not data:
            return 0.0
        
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log2(p_x)
        
        # Normalize to 0-1 range (max entropy for byte is 8 bits)
        return entropy / 8.0
    
    def get_algorithm_info(self):
        """Return algorithm information"""
        return {
            'name': 'AES',
            'key_size': self.key_size,
            'block_size': 128,
            'mode': 'CBC',
            'security_level': 'High' if self.key_size >= 256 else 'Medium'
        }
