import time
import tracemalloc
import psutil
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import math

class ChaCha20Encryption:
    def __init__(self):
        """Initialize ChaCha20 encryption"""
        self.key = None
        self.nonce = None
        
    def generate_key(self):
        """Generate a random ChaCha20 key (256 bits) and nonce (128 bits)"""
        self.key = os.urandom(32)  # 256 bits
        self.nonce = os.urandom(16)  # 128 bits
        return self.key, self.nonce
    
    def set_key(self, key, nonce):
        """Set existing key and nonce"""
        self.key = key
        self.nonce = nonce
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using ChaCha20
        Returns: (ciphertext, encryption_time_ms, cpu_percent, memory_mb, entropy)
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # Start performance monitoring
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=0.1)
        tracemalloc.start()
        start_time = time.time()
        
        # Encryption (ChaCha20 is a stream cipher, no padding needed)
        cipher = Cipher(
            algorithms.ChaCha20(self.key, self.nonce),
            mode=None,
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        
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
        Decrypt ciphertext using ChaCha20
        Returns: (plaintext, decryption_time_ms, cpu_percent, memory_mb)
        """
        # Start performance monitoring
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=0.1)
        tracemalloc.start()
        start_time = time.time()
        
        # Decryption
        cipher = Cipher(
            algorithms.ChaCha20(self.key, self.nonce),
            mode=None,
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
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
            'name': 'ChaCha20',
            'key_size': 256,
            'block_size': None,  # Stream cipher
            'mode': 'Stream',
            'security_level': 'High'
        }
