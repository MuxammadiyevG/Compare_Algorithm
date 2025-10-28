# Texnik Hisobot - Qism 1: Kalitlar va Xavfsizlik Mexanizmlari

## 📋 Umumiy Ma'lumot

**Loyiha nomi:** Intellektual Audit Modeli - Shifrlash Algoritmlari Tahlil Tizimi  
**Muallif:** Dasturiy Ta'minot Xavfsizligi Tahlil Tizimi  
**Sana:** 2024  
**Texnologiyalar:** Python 3.13, Flask 3.0, SQLAlchemy, Cryptography

---

## 🔐 1. SHIFRLASH KALITLARINI YARATISH MEXANIZMI

### 1.1 Key Manager Arxitekturasi

**Fayl:** `modules/key_manager.py`

Key Manager tizimi uch qatlamli xavfsizlik arxitekturasiga asoslangan:

```
┌─────────────────────────────────────┐
│   Application Layer (Flask)         │
├─────────────────────────────────────┤
│   Key Manager (Kalit boshqaruvi)    │
├─────────────────────────────────────┤
│   Encrypted Vault (Shifrlangan xona)│
├─────────────────────────────────────┤
│   Master Key (Asosiy kalit)         │
└─────────────────────────────────────┘
```

### 1.2 Master Key (Asosiy Kalit) Yaratish

**Kod:** `_get_or_create_master_key()` metodi

```python
master_key = os.urandom(32)  # 256-bit kalit
```

**Texnik Qarorlar:**

1. **Nima uchun 256-bit?**
   - AES-256 standartiga mos
   - NIST tomonidan tavsiya etilgan minimal xavfsiz uzunlik
   - 2^256 = 1.15 × 10^77 ta mumkin bo'lgan kombinatsiya
   - Brute-force hujumga qarshi maksimal himoya

2. **Nima uchun `os.urandom()`?**
   - Operatsion tizimning kriptografik xavfsiz random generatori
   - `/dev/urandom` (Linux) yoki `CryptGenRandom` (Windows) dan foydalanadi
   - Pseudo-random emas, haqiqiy entropy manbalaridan foydalanadi
   - FIPS 140-2 standartiga mos

3. **Saqlash joyi:**
   - Fayl: `database/.master_key`
   - Binary formatda (base64 emas)
   - Faqat o'qish huquqi (read-only)
   - `.gitignore` da qo'shilgan (versiya nazoratidan tashqari)

### 1.3 Algoritm-Spetsifik Kalitlar Yaratish

**Kod:** `create_key()` metodi

#### AES Kaliti
```python
key = os.urandom(32)      # 256-bit kalit
iv = os.urandom(16)       # 128-bit IV (Initialization Vector)
```

**Nima uchun shunday?**
- AES blok hajmi har doim 128-bit (16 bayt)
- IV har bir shifrlash uchun noyob bo'lishi kerak
- CBC rejimida IV xavfsizlik uchun zarur
- Bir xil plaintext turli ciphertext beradi

#### DES Kaliti
```python
key = os.urandom(8)       # 64-bit (56-bit effective)
iv = os.urandom(8)        # 64-bit IV
```

**Nima uchun DES qo'shilgan?**
- Tarixiy taqqoslash uchun
- Zaif algoritmlarni ko'rsatish
- Xavfsizlik darajasini taqqoslash
- **ISHLAB CHIQARISHDA ISHLATILMAYDI!**

#### Blowfish Kaliti
```python
key = os.urandom(16)      # 128-bit kalit
iv = os.urandom(8)        # 64-bit IV
```

**Nima uchun 128-bit?**
- Blowfish 32-448 bit qo'llab-quvvatlaydi
- 128-bit optimal balans (xavfsizlik vs tezlik)
- Blowfish blok hajmi 64-bit

#### ChaCha20 Kaliti
```python
key = os.urandom(32)      # 256-bit kalit
nonce = os.urandom(16)    # 128-bit nonce
```

**Nima uchun ChaCha20?**
- Zamonaviy stream cipher
- AES-ga alternativa
- Mobil qurilmalarda tezroq
- Google tomonidan qo'llab-quvvatlanadi

---

## 🔒 2. KALITLARNI SAQLASH MEXANIZMI

### 2.1 Vault Shifrlash Tizimi

**Arxitektura:**

```
Plaintext Keys (JSON)
        ↓
    PKCS7 Padding
        ↓
    AES-256-CBC Encryption
        ↓
    IV + Ciphertext
        ↓
    Encrypted Vault File
```

### 2.2 Vault Shifrlash Algoritmi

**Kod:** `_encrypt_vault()` metodi

```python
# 1. Random IV yaratish
iv = os.urandom(16)

# 2. AES-256-CBC cipher yaratish
cipher = Cipher(
    algorithms.AES(self.master_key),  # 256-bit master key
    modes.CBC(iv),                     # CBC rejimi
    backend=default_backend()
)

# 3. Padding qo'shish (PKCS7)
padder = padding.PKCS7(128).padder()
padded_data = padder.update(data.encode('utf-8')) + padder.finalize()

# 4. Shifrlash
ciphertext = encryptor.update(padded_data) + encryptor.finalize()

# 5. IV + Ciphertext qaytarish
return iv + ciphertext
```

**Texnik Qarorlar:**

1. **Nima uchun CBC rejimi?**
   - Block cipher mode of operation
   - Har bir blok oldingi blokka bog'liq
   - Bir xil bloklar turli ciphertext beradi
   - NIST tavsiya etilgan rejim

2. **Nima uchun PKCS7 padding?**
   - AES blok hajmi 128-bit (16 bayt)
   - Ma'lumot hajmi 16 ga bo'linmasligi mumkin
   - PKCS7 standart padding mexanizmi
   - Avtomatik padding qo'shish va olib tashlash

3. **Nima uchun IV ni ciphertext bilan saqlash?**
   - Deshifrlash uchun IV kerak
   - IV maxfiy emas, faqat noyob bo'lishi kerak
   - Standart amaliyot (best practice)
   - Har safar yangi IV ishlatiladi

### 2.3 JSON Serializatsiya

**Kod:** `_save_keys()` metodi

```python
serializable_keys = {}
for key_id, key_data in self.keys.items():
    serializable_keys[key_id] = {
        'key': base64.b64encode(key_data['key']).decode('utf-8'),
        'iv_or_nonce': base64.b64encode(key_data['iv_or_nonce']).decode('utf-8'),
        'algorithm': key_data['algorithm'],
        'created_at': key_data['created_at'],
        'user': key_data['user']
    }
```

**Nima uchun Base64?**
- Binary ma'lumotni JSON da saqlash uchun
- UTF-8 ga mos
- Standart encoding mexanizmi
- Decode qilish oson

### 2.4 Vault Fayl Strukturasi

**Fayl:** `database/key_vault.enc`

```
[16 bytes IV] + [Variable length encrypted JSON]
```

**Encrypted JSON ichidagi ma'lumot:**
```json
{
  "AES_20241017_120530_123456": {
    "key": "base64_encoded_key",
    "iv_or_nonce": "base64_encoded_iv",
    "algorithm": "AES",
    "created_at": "2024-10-17T12:05:30.123456",
    "user": "admin"
  }
}
```

---

## 🛡️ 3. KALIT BOSHQARUV XAVFSIZLIGI

### 3.1 Key Rotation (Kalit Almashtirish)

**Kod:** `rotate_key()` metodi

```python
def rotate_key(self, old_key_id, user='system'):
    algorithm = self.keys[old_key_id]['algorithm']
    new_key_id = self.create_key(algorithm, user)
    logging.info(f"Key rotated - Old ID: {old_key_id}, New ID: {new_key_id}")
    return new_key_id
```

**Nima uchun rotation kerak?**
- Xavfsizlik best practice
- Eski kalitlar buzilishi mumkin
- Compliance talablari (PCI DSS, HIPAA)
- Forward secrecy ta'minlash

### 3.2 Audit Logging

**Fayl:** `logs/audit.log`

**Kod:**
```python
logging.basicConfig(
    filename=audit_log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

**Loglanuvchi hodisalar:**
- Kalit yaratish: `Key created - ID: {key_id}, Algorithm: {algorithm}`
- Kalit olish: `Key accessed - ID: {key_id}`
- Kalit rotation: `Key rotated - Old ID: {old_key_id}, New ID: {new_key_id}`
- Kalit o'chirish: `Key deleted - ID: {key_id}`

**Nima uchun audit log?**
- Xavfsizlik hodisalarini kuzatish
- Forensic tahlil uchun
- Compliance talablari
- Noqonuniy kirishlarni aniqlash

### 3.3 Access Control

**Kod:**
```python
def get_key(self, key_id):
    if key_id not in self.keys:
        raise ValueError(f"Key not found: {key_id}")
    # Audit log
    logging.info(f"Key accessed - ID: {key_id}")
    return key_data['key'], key_data['iv_or_nonce'], key_data['algorithm']
```

**Xavfsizlik choralari:**
- Kalit mavjudligini tekshirish
- Har bir kirishni loglash
- Faqat zarur ma'lumotni qaytarish
- Exception handling

### 3.4 Key Deletion

**Kod:**
```python
def delete_key(self, key_id, user='system'):
    if key_id not in self.keys:
        raise ValueError(f"Key not found: {key_id}")
    
    algorithm = self.keys[key_id]['algorithm']
    del self.keys[key_id]
    self._save_keys()
    
    logging.info(f"Key deleted - ID: {key_id}, Algorithm: {algorithm}, User: {user}")
```

**Xavfsizlik:**
- Kalit o'chirilgandan keyin vault qayta shiflanadi
- Audit log yoziladi
- Eski kalitni qayta tiklash mumkin emas
- Secure deletion

---

## 🔐 4. MA'LUMOTLAR BAZASI XAVFSIZLIGI

### 4.1 Database Master Key

**Fayl:** `database/models.py`

```python
DB_MASTER_KEY = os.environ.get('DB_MASTER_KEY', os.urandom(32))
```

**Texnik Qarorlar:**

1. **Environment Variable:**
   - Production da `DB_MASTER_KEY` environment variable dan olinadi
   - Development da random key yaratiladi
   - 12-factor app metodologiyasiga mos

2. **Nima uchun alohida master key?**
   - Key vault master key dan mustaqil
   - Defense in depth strategiyasi
   - Bir kalit buzilsa, boshqasi xavfsiz qoladi

### 4.2 User Password Hashing

**Kod:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

**Nima uchun Werkzeug?**
- PBKDF2 algoritmi (default)
- Salt avtomatik qo'shiladi
- Iteration count: 260,000 (2024 standart)
- Rainbow table hujumiga qarshi

**Hash Format:**
```
pbkdf2:sha256:260000$salt$hash
```

### 4.3 Encrypted Data Storage

**Kod:** `EncryptedData` modeli

```python
def set_encrypted_content(self, data):
    # 1. Random IV
    iv = os.urandom(16)
    
    # 2. AES-256-CBC cipher
    cipher = Cipher(
        algorithms.AES(DB_MASTER_KEY[:32]),
        modes.CBC(iv),
        backend=default_backend()
    )
    
    # 3. Padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # 4. Encrypt
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # 5. Store as base64
    self.encrypted_content = base64.b64encode(iv + ciphertext).decode('utf-8')
```

**Nima uchun database da shifrlash?**
- Database dump xavfsiz
- SQL injection hujumida ma'lumot o'qib bo'lmaydi
- Compliance talablari (GDPR, PCI DSS)
- Defense in depth

### 4.4 SQL Injection Himoyasi

**SQLAlchemy ORM:**
```python
# ✅ Xavfsiz (Parameterized query)
User.query.filter_by(username=username).first()

# ❌ Xavfli (String concatenation)
# db.execute(f"SELECT * FROM users WHERE username='{username}'")
```

**Nima uchun ORM?**
- Avtomatik parameterization
- SQL injection himoyasi
- Type safety
- Database-agnostic

---

## 📊 5. XAVFSIZLIK STATISTIKASI

### 5.1 Kalit Xavfsizligi

| Algoritm  | Kalit Hajmi | Mumkin Kombinatsiyalar | Brute-force Vaqti (1 milliard/s) |
|-----------|-------------|------------------------|-----------------------------------|
| AES-256   | 256-bit     | 2^256                  | 3.67 × 10^51 yil                  |
| ChaCha20  | 256-bit     | 2^256                  | 3.67 × 10^51 yil                  |
| Blowfish  | 128-bit     | 2^128                  | 1.08 × 10^13 yil                  |
| DES       | 56-bit      | 2^56                   | 2.28 yil (ZAIF!)                  |

### 5.2 Shifrlash Tezligi vs Xavfsizlik

```
Xavfsizlik ↑
    │
    │  ┌─── AES-256
    │  │
    │  ├─── ChaCha20
    │  │
    │  ├─── Blowfish-128
    │  │
    │  └─── DES (ZAIF)
    │
    └────────────────→ Tezlik
```

---

## 🎯 6. BEST PRACTICES QILLINGAN

### 6.1 OWASP Top 10 Himoyasi

1. ✅ **A02:2021 - Cryptographic Failures**
   - Kuchli algoritmlar (AES-256, ChaCha20)
   - Xavfsiz kalit yaratish (os.urandom)
   - Kalit rotation mexanizmi

2. ✅ **A03:2021 - Injection**
   - SQLAlchemy ORM
   - Parameterized queries
   - Input validation

3. ✅ **A07:2021 - Identification and Authentication Failures**
   - PBKDF2 password hashing
   - Session management
   - Audit logging

### 6.2 NIST Standartlari

- ✅ NIST SP 800-38A (CBC mode)
- ✅ NIST SP 800-132 (Password-based key derivation)
- ✅ NIST SP 800-57 (Key management)

### 6.3 Defense in Depth

```
Layer 1: Application (Flask session, CSRF protection)
Layer 2: Key Management (Encrypted vault, rotation)
Layer 3: Database (Encrypted content, hashed passwords)
Layer 4: File System (Master key file permissions)
Layer 5: Audit (Comprehensive logging)
```

---

## 📝 XULOSA

Ushbu loyihada qo'llangan kalit boshqaruv va xavfsizlik mexanizmlari:

1. **Kriptografik Xavfsizlik:** AES-256, ChaCha20 kabi zamonaviy algoritmlar
2. **Kalit Boshqaruv:** Encrypted vault, rotation, audit logging
3. **Ma'lumotlar Bazasi:** Shifrlangan saqlash, hashed passwords
4. **Best Practices:** OWASP, NIST standartlariga rioya
5. **Defense in Depth:** Ko'p qatlamli himoya strategiyasi

**Keyingi qism:** Shifrlash algoritmlari va tahlil mexanizmlari
