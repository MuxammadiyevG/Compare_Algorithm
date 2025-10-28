# Texnik Hisobot - Qism 2: Shifrlash Algoritmlari va Tahlil Mexanizmlari

## 📋 Umumiy Ma'lumot

Bu qism loyihada qo'llangan shifrlash algoritmlarini, ularning implementatsiyasini va intellektual tahlil modelini batafsil tushuntiradi.

---

## 🔐 1. SHIFRLASH ALGORITMLARI

### 1.1 AES (Advanced Encryption Standard)

**Fayl:** `modules/encryption/aes.py`

#### Texnik Xususiyatlar

```python
class AESEncryption:
    def __init__(self, key_size=256):
        self.key_size = 256  # 128, 192, yoki 256 bit
```

| Xususiyat | Qiymat |
|-----------|--------|
| Algoritm turi | Block cipher |
| Blok hajmi | 128-bit (16 bayt) |
| Kalit hajmi | 256-bit (32 bayt) |
| Rejim | CBC (Cipher Block Chaining) |
| Padding | PKCS7 |
| Xavfsizlik darajasi | Yuqori (High) |

#### Nima uchun AES-256?

1. **NSA tomonidan tasdiqlangan:**
   - TOP SECRET ma'lumotlar uchun
   - US hukumat standarti
   - Butun dunyo bo'ylab qo'llaniladi

2. **Matematik xavfsizlik:**
   - 2^256 = 1.15 × 10^77 kombinatsiya
   - Hozirgi kompyuterlar bilan buzib bo'lmaydi
   - Kvant kompyuterlar uchun ham xavfsiz (Grover algoritmi bilan 2^128)

3. **Tezlik va samaradorlik:**
   - Zamonaviy protsessorlarda AES-NI ko'rsatmalar
   - Hardware acceleration
   - Optimal tezlik va xavfsizlik balansi

#### Implementatsiya Detallari

**Shifrlash jarayoni:**

```python
def encrypt(self, plaintext):
    # 1. Padding qo'shish
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    # 2. Cipher yaratish
    cipher = Cipher(
        algorithms.AES(self.key),  # 256-bit kalit
        modes.CBC(self.iv),         # CBC rejimi
        backend=default_backend()
    )
    
    # 3. Shifrlash
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return ciphertext
```

**Nima uchun CBC rejimi?**

- **Diffusion:** Bir bit o'zgarishi butun blokni o'zgartiradi
- **Avalanche effect:** Kichik o'zgarish katta ta'sir ko'rsatadi
- **Pattern hiding:** Bir xil bloklar turli ciphertext beradi
- **IV dependency:** Har safar yangi IV = yangi ciphertext

**PKCS7 Padding:**

```
Original: "HELLO" (5 bayt)
Block size: 16 bayt
Padding needed: 11 bayt

Padded: "HELLO\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B"
```

---

### 1.2 DES (Data Encryption Standard)

**Fayl:** `modules/encryption/des.py`

#### Texnik Xususiyatlar

| Xususiyat | Qiymat |
|-----------|--------|
| Algoritm turi | Block cipher |
| Blok hajmi | 64-bit (8 bayt) |
| Kalit hajmi | 56-bit (effective) |
| Rejim | CBC |
| Padding | PKCS7 |
| Xavfsizlik darajasi | Past (Low) |

#### Nima uchun DES qo'shilgan?

**⚠️ MUHIM: DES ishlab chiqarishda ishlatilmaydi!**

1. **Tarixiy ahamiyat:**
   - 1977-2001 yillarda standart
   - Kriptografiya tarixini ko'rsatish
   - Zaif algoritmlarni tushunish

2. **Taqqoslash uchun:**
   - Zamonaviy algoritmlar bilan farqni ko'rsatish
   - Xavfsizlik darajasini baholash
   - Tezlik vs xavfsizlik trade-off

3. **Ta'lim maqsadi:**
   - Nima uchun zaif ekanligini ko'rsatish
   - Brute-force hujumga qarshi himoyasizlik
   - Kalit hajmining ahamiyati

#### DES zaiflik tahlili

**Brute-force hujum:**

```
Kalit hajmi: 56-bit
Kombinatsiyalar: 2^56 = 72,057,594,037,927,936
Tezlik: 1 milliard kalit/soniya
Vaqt: ~2.28 yil

Zamonaviy GPU bilan: bir necha kun!
```

**Implementatsiya:**

```python
from Crypto.Cipher import DES

def encrypt(self, plaintext):
    cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
    padded_data = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext
```

---

### 1.3 Blowfish

**Fayl:** `modules/encryption/blowfish.py`

#### Texnik Xususiyatlar

| Xususiyat | Qiymat |
|-----------|--------|
| Algoritm turi | Block cipher |
| Blok hajmi | 64-bit (8 bayt) |
| Kalit hajmi | 128-bit (loyihada) |
| Kalit diapazoni | 32-448 bit |
| Rejim | CBC |
| Xavfsizlik darajasi | O'rta (Medium) |

#### Nima uchun Blowfish?

1. **Tezlik:**
   - Juda tez shifrlash
   - Kichik qurilmalar uchun mos
   - Kam resurs talab qiladi

2. **Moslashuvchanlik:**
   - 32 dan 448 bit gacha kalit
   - Turli xavfsizlik talablari uchun
   - Optimal hajmni tanlash imkoniyati

3. **Patent-free:**
   - Bepul va ochiq
   - Litsenziya to'lovi yo'q
   - Keng qo'llaniladi

#### Blowfish vs AES

```
Blowfish afzalliklari:
+ Tezroq (ba'zi platformalarda)
+ Moslashuvchan kalit hajmi
+ Oddiy implementatsiya

AES afzalliklari:
+ Standartlashtirilgan
+ Hardware acceleration
+ Keng qo'llab-quvvatlanadi
+ Zamonaviy
```

**Implementatsiya:**

```python
from Crypto.Cipher import Blowfish

def encrypt(self, plaintext):
    cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv)
    padded_data = pad(plaintext, Blowfish.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext
```

---

### 1.4 ChaCha20

**Fayl:** `modules/encryption/chacha20.py`

#### Texnik Xususiyatlar

| Xususiyat | Qiymat |
|-----------|--------|
| Algoritm turi | Stream cipher |
| Kalit hajmi | 256-bit |
| Nonce hajmi | 128-bit |
| Blok hajmi | Yo'q (stream) |
| Padding | Kerak emas |
| Xavfsizlik darajasi | Yuqori (High) |

#### Nima uchun ChaCha20?

1. **Zamonaviy dizayn:**
   - 2008 yilda Daniel J. Bernstein tomonidan yaratilgan
   - Salsa20 ning yaxshilangan versiyasi
   - Google tomonidan qo'llab-quvvatlanadi

2. **Mobil qurilmalar uchun:**
   - AES-NI bo'lmagan qurilmalarda tezroq
   - ARM protsessorlarda optimal
   - Kam energiya sarfi

3. **TLS 1.3 da ishlatiladi:**
   - IETF standart
   - ChaCha20-Poly1305 AEAD
   - Cloudflare, Google ishlatadi

#### Stream Cipher vs Block Cipher

**Block Cipher (AES):**
```
Plaintext: [Block1][Block2][Block3]
              ↓        ↓        ↓
Ciphertext: [Cipher1][Cipher2][Cipher3]
```

**Stream Cipher (ChaCha20):**
```
Plaintext:  H  E  L  L  O
Keystream:  X  Y  Z  A  B
              ⊕  ⊕  ⊕  ⊕  ⊕
Ciphertext: C1 C2 C3 C4 C5
```

**Implementatsiya:**

```python
def encrypt(self, plaintext):
    # Padding kerak emas!
    cipher = Cipher(
        algorithms.ChaCha20(self.key, self.nonce),
        mode=None,  # Stream cipher
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext
```

---

## 📊 2. PERFORMANCE MONITORING

### 2.1 Vaqt O'lchash

**Kod:**

```python
import time

start_time = time.time()
# Shifrlash jarayoni
end_time = time.time()

encryption_time = (end_time - start_time) * 1000  # millisekund
```

**Nima uchun millisekund?**
- Aniqroq o'lchash
- Kichik farqlarni ko'rish
- Standart metrika

### 2.2 CPU Monitoring

**Kod:**

```python
import psutil

process = psutil.Process()
cpu_before = process.cpu_percent(interval=0.1)
# Shifrlash jarayoni
cpu_after = process.cpu_percent(interval=0.1)

cpu_usage = (cpu_before + cpu_after) / 2
```

**Nima uchun psutil?**
- Cross-platform (Windows, Linux, macOS)
- Real-time monitoring
- Process-specific metrics
- Aniq va ishonchli

### 2.3 Memory Monitoring

**Kod:**

```python
import tracemalloc

tracemalloc.start()
# Shifrlash jarayoni
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

memory_usage = peak / (1024 * 1024)  # MB
```

**Nima uchun tracemalloc?**
- Python-specific memory tracking
- Peak memory detection
- Memory leak detection
- Aniq o'lchash

### 2.4 Entropy Calculation

**Shannon Entropy formulasi:**

```
H(X) = -Σ P(xi) * log2(P(xi))
```

**Implementatsiya:**

```python
def _calculate_entropy(self, data):
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    
    # Normalize to 0-1 range
    return entropy / 8.0
```

**Nima uchun entropy?**
- Randomness o'lchovi
- Yaxshi shifrlash = yuqori entropy
- Xavfsizlik ko'rsatkichi
- 0-1 oralig'ida normallashtirilgan

**Entropy qiymatlari:**

```
0.0 - 0.3: Juda zaif (predictable)
0.3 - 0.6: Zaif
0.6 - 0.8: O'rtacha
0.8 - 0.95: Yaxshi
0.95 - 1.0: Juda yaxshi (random)
```

---

## 🧮 3. INTELLEKTUAL AUDIT MODELI

### 3.1 Model Formulasi

**Asosiy formula:**

```
S = w1·T + w2·E + w3·K + w4·I
```

Bu yerda:
- **S** - Umumiy samaradorlik balli (Overall Score)
- **T** - Tezlik ko'rsatkichi (Performance)
- **E** - Xavfsizlik ko'rsatkichi (Security)
- **K** - Kalit boshqaruv ko'rsatkichi (Key Management)
- **I** - Yaxlitlik ko'rsatkichi (Integrity)
- **w1, w2, w3, w4** - Vazn koeffitsientlari

### 3.2 Vazn Koeffitsientlari

**Fayl:** `config.py`

```python
WEIGHT_PERFORMANCE = 0.25      # w1 = 25%
WEIGHT_SECURITY = 0.35         # w2 = 35%
WEIGHT_KEY_MANAGEMENT = 0.25   # w3 = 25%
WEIGHT_INTEGRITY = 0.15        # w4 = 15%
```

**Nima uchun shunday taqsimlash?**

1. **Security (35%)** - Eng muhim
   - Xavfsizlik birinchi o'rinda
   - Zaif shifrlash = foydasiz
   - Compliance talablari

2. **Performance (25%)** - Muhim
   - Tezlik va samaradorlik
   - User experience
   - Scalability

3. **Key Management (25%)** - Muhim
   - Kalit boshqaruv qulayligi
   - Operational overhead
   - Maintenance cost

4. **Integrity (15%)** - Zarur
   - Ma'lumot yaxlitligi
   - Error detection
   - Reliability

### 3.3 T - Performance Score

**Formula:**

```
T = 0.5·T_time + 0.3·T_cpu + 0.2·T_memory
```

**Implementatsiya:**

```python
def _calculate_performance_score(self, metrics):
    # Time score (max 100ms for good performance)
    time_score = max(0, 1 - (metrics['total_time_ms'] / 100))
    
    # CPU score (max 50% for good performance)
    cpu_score = max(0, 1 - (metrics['avg_cpu_percent'] / 50))
    
    # Memory score (max 10MB for good performance)
    mem_score = max(0, 1 - (metrics['avg_memory_mb'] / 10))
    
    # Weighted average
    T = (time_score * 0.5 + cpu_score * 0.3 + mem_score * 0.2)
    
    return min(1.0, max(0.0, T))
```

**Normalizatsiya:**
- Barcha qiymatlar 0-1 oralig'ida
- Kichik qiymat = yaxshi performance
- Inverse relationship

**Benchmark qiymatlari:**

| Metrika | Yaxshi | O'rtacha | Yomon |
|---------|--------|----------|-------|
| Vaqt | < 50ms | 50-100ms | > 100ms |
| CPU | < 25% | 25-50% | > 50% |
| RAM | < 5MB | 5-10MB | > 10MB |

### 3.4 E - Security Score

**Formula:**

```
E = 0.4·E_key + 0.3·E_entropy + 0.3·E_level
```

**Implementatsiya:**

```python
def _calculate_security_score(self, metrics):
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
    
    # Entropy score (already 0-1)
    entropy_score = metrics['entropy']
    
    # Security level score
    security_level = metrics['security_level']
    if security_level == 'High':
        level_score = 1.0
    elif security_level == 'Medium':
        level_score = 0.6
    else:
        level_score = 0.3
    
    E = (key_score * 0.4 + entropy_score * 0.3 + level_score * 0.3)
    return min(1.0, max(0.0, E))
```

**Xavfsizlik darajalari:**

| Kalit Hajmi | Daraja | Ball |
|-------------|--------|------|
| ≥ 256 bit | High | 1.0 |
| 128-255 bit | Medium | 0.8 |
| 64-127 bit | Low | 0.5 |
| < 64 bit | Very Low | 0.3 |

### 3.5 K - Key Management Score

**Formula:**

```
K = 0.5·K_size + 0.5·K_complexity
```

**Implementatsiya:**

```python
def _calculate_key_management_score(self, metrics):
    key_size = metrics['key_size']
    algorithm = metrics['algorithm']
    
    # Key size manageability (larger = harder to manage)
    if key_size <= 128:
        size_score = 1.0
    elif key_size <= 256:
        size_score = 0.9
    else:
        size_score = 0.8
    
    # Algorithm complexity
    if algorithm in ['ChaCha20', 'AES']:
        complexity_score = 0.9  # Modern, well-supported
    elif algorithm == 'Blowfish':
        complexity_score = 0.7
    else:  # DES
        complexity_score = 0.5  # Outdated
    
    K = (size_score * 0.5 + complexity_score * 0.5)
    return min(1.0, max(0.0, K))
```

**Nima uchun katta kalit = qiyinroq boshqaruv?**
- Ko'proq storage
- Sekinroq operatsiyalar
- Ko'proq bandwidth
- Lekin xavfsizroq!

### 3.6 I - Integrity Score

**Formula:**

```
I = 0.5·I_check + 0.3·I_entropy + 0.2·I_size
```

**Implementatsiya:**

```python
def _calculate_integrity_score(self, metrics):
    # Integrity check (successful decryption)
    integrity_score = 1.0 if metrics['integrity_check'] else 0.0
    
    # Entropy (high = good)
    entropy_score = metrics['entropy']
    
    # Size consistency
    size_ratio = metrics['ciphertext_size'] / max(metrics['plaintext_size'], 1)
    size_score = 1.0 if 1.0 <= size_ratio <= 2.0 else 0.8
    
    I = (integrity_score * 0.5 + entropy_score * 0.3 + size_score * 0.2)
    return min(1.0, max(0.0, I))
```

**Integrity tekshiruvi:**
- Shifrlash → Deshifrlash → Taqqoslash
- Original == Decrypted → Success
- Original != Decrypted → Failure

---

## 📈 4. TAHLIL JARAYONI

### 4.1 Bitta Algoritm Tahlili

**Kod:** `analyze_algorithm()` metodi

```python
def analyze_algorithm(self, algorithm_name, plaintext, key=None, iv_or_nonce=None):
    # 1. Algoritm yaratish
    algo = AESEncryption(key_size=256)  # Misol
    
    # 2. Kalit yaratish/o'rnatish
    if key and iv_or_nonce:
        algo.set_key(key, iv_or_nonce)
    else:
        key, iv_or_nonce = algo.generate_key()
    
    # 3. Shifrlash
    ciphertext, enc_time, enc_cpu, enc_mem, entropy = algo.encrypt(plaintext)
    
    # 4. Deshifrlash
    decrypted, dec_time, dec_cpu, dec_mem = algo.decrypt(ciphertext)
    
    # 5. Yaxlitlik tekshiruvi
    integrity_check = (decrypted == plaintext_bytes)
    
    # 6. Metrikalarni hisoblash
    T = self._calculate_performance_score(metrics)
    E = self._calculate_security_score(metrics)
    K = self._calculate_key_management_score(metrics)
    I = self._calculate_integrity_score(metrics)
    
    # 7. Umumiy ball
    S = self.w1 * T + self.w2 * E + self.w3 * K + self.w4 * I
    
    return metrics, key, iv_or_nonce
```

### 4.2 Barcha Algoritmlarni Taqqoslash

**Kod:** `compare_algorithms()` metodi

```python
def compare_algorithms(self, plaintext):
    algorithms = ['AES', 'DES', 'Blowfish', 'ChaCha20']
    results = []
    
    for algo_name in algorithms:
        try:
            metrics, _, _ = self.analyze_algorithm(algo_name, plaintext)
            results.append(metrics)
        except Exception as e:
            print(f"Error analyzing {algo_name}: {str(e)}")
    
    return results
```

### 4.3 Eng Yaxshi Algoritmni Aniqlash

**Kod:** `get_best_algorithm()` metodi

```python
def get_best_algorithm(self, results):
    if not results:
        return None
    
    best = max(results, key=lambda x: x['S_overall_score'])
    return best['algorithm']
```

---

## 📊 5. NATIJALAR TAHLILI

### 5.1 Kutilgan Natijalar

**Odatiy test ma'lumoti (50 bayt matn):**

| Algoritm | S (Umumiy) | T (Tezlik) | E (Xavfsizlik) | K (Kalit) | I (Yaxlitlik) |
|----------|------------|------------|----------------|-----------|---------------|
| AES-256 | 0.8500 | 0.9200 | 0.9500 | 0.9000 | 0.9800 |
| ChaCha20 | 0.8400 | 0.9500 | 0.9300 | 0.9000 | 0.9700 |
| Blowfish | 0.7200 | 0.8800 | 0.7400 | 0.7000 | 0.9500 |
| DES | 0.4500 | 0.9000 | 0.3000 | 0.5000 | 0.9200 |

**Tahlil:**

1. **AES-256** - Eng yaxshi umumiy ball
   - Yuqori xavfsizlik
   - Yaxshi tezlik
   - Optimal balans

2. **ChaCha20** - Eng tez
   - Mobil qurilmalarda eng yaxshi
   - Yaxshi xavfsizlik
   - Zamonaviy

3. **Blowfish** - O'rtacha
   - Yaxshi tezlik
   - O'rtacha xavfsizlik
   - Legacy tizimlar uchun

4. **DES** - Eng zaif
   - Zaif xavfsizlik
   - Ishlatilmasligi kerak
   - Faqat taqqoslash uchun

### 5.2 Vizualizatsiya

**Bar Chart - Umumiy Ballar:**
```
AES-256   ████████████████████ 0.85
ChaCha20  ███████████████████▌ 0.84
Blowfish  ██████████████▌       0.72
DES       █████████             0.45
```

**Radar Chart - Ko'rsatkichlar:**
```
        Tezlik
          /\
         /  \
        /    \
  Kalit      Xavfsizlik
        \    /
         \  /
          \/
      Yaxlitlik
```

---

## 🎯 6. XULOSA

### 6.1 Asosiy Yutuqlar

1. ✅ **4 ta algoritm implementatsiyasi**
   - AES-256, DES, Blowfish, ChaCha20
   - To'liq performance monitoring
   - Entropy calculation

2. ✅ **Intellektual tahlil modeli**
   - 4 ta asosiy metrika
   - Vazn koeffitsientlari
   - Normallashtirilgan ballar

3. ✅ **Real-time monitoring**
   - CPU, Memory, Time tracking
   - Aniq va ishonchli
   - Cross-platform

### 6.2 Tavsiyalar

**Production uchun:**
- ✅ AES-256 yoki ChaCha20 ishlatish
- ❌ DES ishlatmaslik
- ⚠️ Blowfish ehtiyotkorlik bilan

**Keyingi qism:** Web interfeys, ma'lumotlar bazasi va deployment
