import time
import tracemalloc
import psutil
import os
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
import math

class BlowfishEncryption:
    def __init__(self, key_size=128):
        """
        Initialize Blowfish encryption with specified key size (32-448 bits)
        Default: 128 bits
        """
        self.key_size = key_size
        self.key = None
        self.iv = None
        
    def generate_key(self):
        """Generate a random Blowfish key"""
        self.key = os.urandom(self.key_size // 8)
        self.iv = os.urandom(8)  # Blowfish block size is 8 bytes
        return self.key, self.iv
    
    def set_key(self, key, iv):
        """Set existing key and IV"""
        self.key = key
        self.iv = iv
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using Blowfish-CBC
        Returns: (ciphertext, encryption_time_ms, cpu_percent, memory_mb, entropy)
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # Start performance monitoring
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=0.1)
        tracemalloc.start()
        start_time = time.time()
        
        # Encryption
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv)
        padded_data = pad(plaintext, Blowfish.block_size)
        ciphertext = cipher.encrypt(padded_data)
        
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
        Decrypt ciphertext using Blowfish-CBC
        Returns: (plaintext, decryption_time_ms, cpu_percent, memory_mb)
        """
        # Start performance monitoring
        process = psutil.Process()
        cpu_before = process.cpu_percent(interval=0.1)
        tracemalloc.start()
        start_time = time.time()
        
        # Decryption
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, Blowfish.block_size)
        
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
            'name': 'Blowfish',
            'key_size': self.key_size,
            'block_size': 64,
            'mode': 'CBC',
            'security_level': 'Medium'
        }
