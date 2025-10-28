from modules.encryption.aes import AESEncryption
from modules.encryption.des import DESEncryption
from modules.encryption.blowfish import BlowfishEncryption
from modules.encryption.chacha20 import ChaCha20Encryption

class EncryptionAnalyzer:
    def __init__(self, config):
        """
        Initialize analyzer with configuration weights
        """
        self.w1 = config.WEIGHT_PERFORMANCE
        self.w2 = config.WEIGHT_SECURITY
        self.w3 = config.WEIGHT_KEY_MANAGEMENT
        self.w4 = config.WEIGHT_INTEGRITY
    
    def analyze_algorithm(self, algorithm_name, plaintext, key=None, iv_or_nonce=None):
        """
        Analyze a specific encryption algorithm
        Returns: dictionary with all metrics
        """
        # Initialize algorithm
        if algorithm_name == 'AES':
            algo = AESEncryption(key_size=256)
        elif algorithm_name == 'DES':
            algo = DESEncryption()
        elif algorithm_name == 'Blowfish':
            algo = BlowfishEncryption(key_size=128)
        elif algorithm_name == 'ChaCha20':
            algo = ChaCha20Encryption()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm_name}")
        
        # Generate or set key
        if key and iv_or_nonce:
            algo.set_key(key, iv_or_nonce)
        else:
            key, iv_or_nonce = algo.generate_key()
        
        # Encrypt
        ciphertext, enc_time, enc_cpu, enc_mem, entropy = algo.encrypt(plaintext)
        
        # Decrypt
        decrypted, dec_time, dec_cpu, dec_mem = algo.decrypt(ciphertext)
        
        # Verify integrity
        if isinstance(plaintext, str):
            plaintext_bytes = plaintext.encode('utf-8')
        else:
            plaintext_bytes = plaintext
        
        integrity_check = (decrypted == plaintext_bytes)
        
        # Calculate metrics
        metrics = {
            'algorithm': algorithm_name,
            'encryption_time_ms': round(enc_time, 4),
            'decryption_time_ms': round(dec_time, 4),
            'total_time_ms': round(enc_time + dec_time, 4),
            'avg_cpu_percent': round((enc_cpu + dec_cpu) / 2, 2),
            'avg_memory_mb': round((enc_mem + dec_mem) / 2, 4),
            'entropy': round(entropy, 4),
            'integrity_check': integrity_check,
            'key_size': algo.get_algorithm_info()['key_size'],
            'security_level': algo.get_algorithm_info()['security_level'],
            'plaintext_size': len(plaintext_bytes),
            'ciphertext_size': len(ciphertext)
        }
        
        # Calculate normalized scores (0-1 range)
        T = self._calculate_performance_score(metrics)
        E = self._calculate_security_score(metrics)
        K = self._calculate_key_management_score(metrics)
        I = self._calculate_integrity_score(metrics)
        
        # Calculate overall efficiency score
        S = self.w1 * T + self.w2 * E + self.w3 * K + self.w4 * I
        
        metrics['T_performance'] = round(T, 4)
        metrics['E_security'] = round(E, 4)
        metrics['K_key_management'] = round(K, 4)
        metrics['I_integrity'] = round(I, 4)
        metrics['S_overall_score'] = round(S, 4)
        
        return metrics, key, iv_or_nonce
    
    def _calculate_performance_score(self, metrics):
        """
        Calculate performance efficiency score (T)
        Lower time and resource usage = higher score
        """
        # Normalize time (assuming max 100ms for good performance)
        time_score = max(0, 1 - (metrics['total_time_ms'] / 100))
        
        # Normalize CPU (assuming max 50% for good performance)
        cpu_score = max(0, 1 - (metrics['avg_cpu_percent'] / 50))
        
        # Normalize memory (assuming max 10MB for good performance)
        mem_score = max(0, 1 - (metrics['avg_memory_mb'] / 10))
        
        # Weighted average
        T = (time_score * 0.5 + cpu_score * 0.3 + mem_score * 0.2)
        
        return min(1.0, max(0.0, T))
    
    def _calculate_security_score(self, metrics):
        """
        Calculate security strength score (E)
        Based on key size and entropy
        """
        # Key size score
        key_size = metrics['key_size']
        if key_size >= 256:
            key_score = 1.0
        elif key_size >= 128:
            key_score = 0.8
        elif key_size >= 64:
            key_score = 0.5
        else:
            key_score = 0.3
        
        # Entropy score (already normalized 0-1)
        entropy_score = metrics['entropy']
        
        # Security level score
        security_level = metrics['security_level']
        if security_level == 'High':
            level_score = 1.0
        elif security_level == 'Medium':
            level_score = 0.6
        else:
            level_score = 0.3
        
        # Weighted average
        E = (key_score * 0.4 + entropy_score * 0.3 + level_score * 0.3)
        
        return min(1.0, max(0.0, E))
    
    def _calculate_key_management_score(self, metrics):
        """
        Calculate key management efficiency score (K)
        Based on key size and algorithm complexity
        """
        key_size = metrics['key_size']
        algorithm = metrics['algorithm']
        
        # Key size manageability (larger keys are harder to manage)
        if key_size <= 128:
            size_score = 1.0
        elif key_size <= 256:
            size_score = 0.9
        else:
            size_score = 0.8
        
        # Algorithm complexity score
        if algorithm in ['ChaCha20', 'AES']:
            complexity_score = 0.9  # Modern, well-supported
        elif algorithm == 'Blowfish':
            complexity_score = 0.7
        else:  # DES
            complexity_score = 0.5  # Outdated
        
        K = (size_score * 0.5 + complexity_score * 0.5)
        
        return min(1.0, max(0.0, K))
    
    def _calculate_integrity_score(self, metrics):
        """
        Calculate integrity and reliability score (I)
        Based on successful decryption and entropy
        """
        # Integrity check
        integrity_score = 1.0 if metrics['integrity_check'] else 0.0
        
        # Entropy (high entropy = good)
        entropy_score = metrics['entropy']
        
        # Size consistency
        size_ratio = metrics['ciphertext_size'] / max(metrics['plaintext_size'], 1)
        size_score = 1.0 if 1.0 <= size_ratio <= 2.0 else 0.8
        
        I = (integrity_score * 0.5 + entropy_score * 0.3 + size_score * 0.2)
        
        return min(1.0, max(0.0, I))
    
    def compare_algorithms(self, plaintext):
        """
        Compare all algorithms with the same plaintext
        Returns: list of metrics for all algorithms
        """
        algorithms = ['AES', 'DES', 'Blowfish', 'ChaCha20']
        results = []
        
        for algo_name in algorithms:
            try:
                metrics, _, _ = self.analyze_algorithm(algo_name, plaintext)
                results.append(metrics)
            except Exception as e:
                print(f"Error analyzing {algo_name}: {str(e)}")
        
        return results
    
    def get_best_algorithm(self, results):
        """
        Determine the best algorithm based on overall score
        """
        if not results:
            return None
        
        best = max(results, key=lambda x: x['S_overall_score'])
        return best['algorithm']
