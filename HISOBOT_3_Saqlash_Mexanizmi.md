# Texnik Hisobot - Qism 3: Shifrlangan Ma'lumotlarni Saqlash Mexanizmi

## 📋 Umumiy Ma'lumot

Bu qism loyihada shifrlangan matn va fayllarning qayerga, qanday formatda va qanday xavfsizlik choralari bilan saqlanayotganini batafsil tushuntiradi.

---

## 💾 1. SAQLASH ARXITEKTURASI

### 1.1 Uch Qatlamli Saqlash Tizimi

```
┌─────────────────────────────────────────────┐
│  Layer 1: Application Memory (Vaqtinchalik) │
│  - Flask session                             │
│  - Python variables                          │
│  - Faqat tahlil vaqtida                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 2: Database (Doimiy)                 │
│  - SQLite database                           │
│  - Shifrlangan saqlash                       │
│  - User-specific data                        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Layer 3: File System (Doimiy)              │
│  - Key vault (shifrlangan)                  │
│  - Audit logs                                │
│  - Uploaded files (vaqtinchalik)            │
└─────────────────────────────────────────────┘
```

---

## 🗄️ 2. MA'LUMOTLAR BAZASI SAQLASH

### 2.1 Database Fayl Joylashuvi

**Fayl:** `encryption_audit.db`  
**Yo'l:** Loyiha root direktoriyasi  
**Turi:** SQLite3 database  
**Hajmi:** Dinamik (foydalanishga qarab)

### 2.2 Database Strukturasi

#### Jadvallar:

1. **users** - Foydalanuvchilar
2. **analysis_results** - Tahlil natijalari
3. **encrypted_data** - Shifrlangan ma'lumotlar
4. **audit_logs** - Audit loglar

### 2.3 EncryptedData Jadvali

**Fayl:** `database/models.py`

```python
class EncryptedData(db.Model):
    __tablename__ = 'encrypted_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    algorithm = db.Column(db.String(50))
    
    # Shifrlangan kontent (base64 formatda)
    encrypted_content = db.Column(db.Text, nullable=False)
    
    # Kalit ID (key_vault da saqlangan)
    key_id = db.Column(db.String(100), nullable=False)
    
    # Metadata
    original_filename = db.Column(db.String(255))
    content_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Jadval strukturasi:**

| Ustun | Turi | Tavsif |
|-------|------|--------|
| id | INTEGER | Primary key (avtomatik) |
| user_id | INTEGER | Foydalanuvchi ID |
| algorithm | VARCHAR(50) | Algoritm nomi (AES, DES, etc.) |
| encrypted_content | TEXT | Shifrlangan kontent (base64) |
| key_id | VARCHAR(100) | Kalit identifikatori |
| original_filename | VARCHAR(255) | Asl fayl nomi (agar fayl bo'lsa) |
| content_type | VARCHAR(50) | Kontent turi (text, file) |
| created_at | DATETIME | Yaratilgan vaqt |

---

## 🔐 3. SHIFRLANGAN MA'LUMOTLARNI SAQLASH JARAYONI

### 3.1 Matn Shifrlash va Saqlash

**API Endpoint:** `POST /encrypt`

**Jarayon:**

```python
# 1. Foydalanuvchi matn kiritadi
plaintext = request.form.get('plaintext')
algorithm = request.form.get('algorithm')  # AES, DES, etc.

# 2. Kalit yaratiladi va key_vault ga saqlanadi
key_id = key_manager.create_key(algorithm, current_user.username)
# key_id format: "AES_20241017_120530_123456"

# 3. Kalit olinadi
key, iv_or_nonce, _ = key_manager.get_key(key_id)

# 4. Matn shiflanadi (algoritm bilan)
result, _, _ = analyzer.analyze_algorithm(algorithm, plaintext, key, iv_or_nonce)

# 5. EncryptedData obyekti yaratiladi
encrypted_data = EncryptedData(
    user_id=current_user.id,
    algorithm=algorithm,
    key_id=key_id,
    content_type='text'
)

# 6. Shifrlangan kontent saqlanadi
encrypted_data.set_encrypted_content(plaintext)

# 7. Database ga yoziladi
db.session.add(encrypted_data)
db.session.commit()
```

### 3.2 set_encrypted_content() Metodi

**Ikki Qatlamli Shifrlash:**

```python
def set_encrypted_content(self, data):
    """
    Ma'lumotni shifrlash va saqlash
    1-qadam: Tanlangan algoritm bilan shifrlash (AES/DES/etc.)
    2-qadam: Database master key bilan qayta shifrlash
    """
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # QADAM 1: Database master key bilan shifrlash
    iv = os.urandom(16)  # Random IV
    
    cipher = Cipher(
        algorithms.AES(DB_MASTER_KEY[:32]),  # 256-bit master key
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    
    # PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # Shifrlash
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # QADAM 2: Base64 encoding (database uchun)
    self.encrypted_content = base64.b64encode(iv + ciphertext).decode('utf-8')
```

**Nima uchun ikki marta shifrlash?**

1. **Birinchi shifrlash:** Foydalanuvchi tanlagan algoritm
   - Tahlil uchun
   - Algoritmlarni taqqoslash
   - Performance o'lchash

2. **Ikkinchi shifrlash:** Database master key
   - Database dump xavfsizligi
   - SQL injection himoyasi
   - Defense in depth

### 3.3 Saqlash Formati

**Database da saqlangan ma'lumot:**

```
encrypted_content = "base64_encoded_string"
```

**Base64 ichidagi struktura:**

```
[16 bytes IV] + [Variable length ciphertext]
```

**Misol:**

```
Original plaintext: "Bu maxfiy matn"
↓
UTF-8 bytes: b'Bu maxfiy matn'
↓
PKCS7 padding: b'Bu maxfiy matn\x02\x02'
↓
AES-256-CBC encryption: [binary ciphertext]
↓
IV + ciphertext: [16 bytes IV][ciphertext]
↓
Base64 encoding: "SGVsbG8gV29ybGQhIFRoaXMgaXMgYSB0ZXN0..."
↓
Database TEXT column: "SGVsbG8gV29ybGQhIFRoaXMgaXMgYSB0ZXN0..."
```

---

## 🔓 4. DESHIFRLASH JARAYONI

### 4.1 Ma'lumotni Qaytarish

**API Endpoint:** `POST /decrypt/<encrypted_id>`

**Jarayon:**

```python
# 1. Database dan shifrlangan ma'lumot olinadi
encrypted_data = EncryptedData.query.get_or_404(encrypted_id)

# 2. Foydalanuvchi huquqi tekshiriladi
if encrypted_data.user_id != current_user.id:
    return jsonify({'error': 'Ruxsat yo\'q!'}), 403

# 3. Kalit olinadi (key_vault dan)
key, iv_or_nonce, algorithm = key_manager.get_key(encrypted_data.key_id)

# 4. Ma'lumot deshifrlanadi
plaintext = encrypted_data.get_decrypted_content()

# 5. Foydalanuvchiga qaytariladi
return jsonify({
    'success': True,
    'plaintext': plaintext.decode('utf-8'),
    'algorithm': algorithm
})
```

### 4.2 get_decrypted_content() Metodi

```python
def get_decrypted_content(self):
    """
    Shifrlangan ma'lumotni deshifrlash
    Teskari jarayon: Base64 → Decrypt → Unpad
    """
    
    # QADAM 1: Base64 decode
    encrypted_data = base64.b64decode(self.encrypted_content)
    
    # QADAM 2: IV va ciphertext ajratish
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    # QADAM 3: AES deshifrlash
    cipher = Cipher(
        algorithms.AES(DB_MASTER_KEY[:32]),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # QADAM 4: Padding olib tashlash
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext
```

---

## 📁 5. FAYL YUKLASH VA SAQLASH

### 5.1 Upload Direktoriyasi

**Yo'l:** `uploads/`  
**Maqsad:** Vaqtinchalik fayl saqlash  
**Xavfsizlik:** `.gitignore` da qo'shilgan

### 5.2 Fayl Yuklash Jarayoni

```python
# 1. Fayl yuklash
file = request.files['file']
filename = secure_filename(file.filename)

# 2. Faylni o'qish
plaintext = file.read()

# 3. Tahlil qilish
results = analyzer.compare_algorithms(plaintext)

# 4. Agar saqlash kerak bo'lsa
encrypted_data = EncryptedData(
    user_id=current_user.id,
    algorithm=algorithm,
    key_id=key_id,
    original_filename=filename,
    content_type='file'
)
encrypted_data.set_encrypted_content(plaintext)
db.session.add(encrypted_data)
db.session.commit()
```

**Muhim:** Fayl o'zi disk ga saqlanmaydi, faqat shifrlangan holda database ga yoziladi!

### 5.3 Nima uchun faylni disk ga saqlamaymiz?

1. **Xavfsizlik:**
   - Disk ga yozilgan fayl o'qilishi mumkin
   - File system permissions bypass qilinishi mumkin
   - Database shifrlangan

2. **Markazlashtirilgan boshqaruv:**
   - Barcha ma'lumot bir joyda
   - Backup oson
   - Migration oson

3. **Access control:**
   - Database orqali faqat ruxsat berilgan foydalanuvchi kiradi
   - SQL injection himoyasi
   - Audit logging

---

## 🔑 6. KALIT SAQLASH (KEY VAULT)

### 6.1 Key Vault Fayl

**Fayl:** `database/key_vault.enc`  
**Format:** Binary (shifrlangan)  
**Shifrlash:** AES-256-CBC (master key bilan)

### 6.2 Key Vault Strukturasi

**Ichki format (deshifrlanganidan keyin):**

```json
{
  "AES_20241017_120530_123456": {
    "key": "base64_encoded_256bit_key",
    "iv_or_nonce": "base64_encoded_iv",
    "algorithm": "AES",
    "created_at": "2024-10-17T12:05:30.123456",
    "user": "admin"
  },
  "ChaCha20_20241017_120545_789012": {
    "key": "base64_encoded_256bit_key",
    "iv_or_nonce": "base64_encoded_nonce",
    "algorithm": "ChaCha20",
    "created_at": "2024-10-17T12:05:45.789012",
    "user": "admin"
  }
}
```

### 6.3 Master Key Fayl

**Fayl:** `database/.master_key`  
**Format:** Binary (32 bayt)  
**Xavfsizlik:** 
- `.gitignore` da
- Faqat o'qish huquqi
- Backup qilinmaydi

---

## 📊 7. TAHLIL NATIJALARI SAQLASH

### 7.1 AnalysisResult Jadvali

**Maqsad:** Tahlil natijalarini tarixiy saqlash

```python
class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    algorithm = db.Column(db.String(50))
    
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
    
    created_at = db.Column(db.DateTime)
```

**Nima saqlanadi:**

1. ✅ Tahlil metrikalari (vaqt, CPU, RAM)
2. ✅ Xavfsizlik ko'rsatkichlari (entropy, key size)
3. ✅ Hisoblangan ballar (T, E, K, I, S)
4. ❌ Asl matn (plaintext) - xavfsizlik uchun
5. ❌ Shifrlangan matn (ciphertext) - hajm uchun
6. ❌ Kalitlar - alohida key_vault da

### 7.2 Session Storage

**Vaqtinchalik saqlash:**

```python
# Tahlil natijalarini session ga saqlash
session['last_analysis'] = results

# Report sahifasida ishlatish
results = session.get('last_analysis')
```

**Nima uchun session?**
- Tez kirish
- Database yuklamaslik
- Faqat joriy sessiya uchun
- Avtomatik tozalanadi

---

## 📝 8. AUDIT LOGGING

### 8.1 Audit Log Fayl

**Fayl:** `logs/audit.log`  
**Format:** Text (timestamp + message)  
**Maqsad:** Xavfsizlik hodisalarini kuzatish

### 8.2 Log Format

```
2024-10-17 12:05:30 - INFO - Key created - ID: AES_20241017_120530_123456, Algorithm: AES, User: admin
2024-10-17 12:05:35 - INFO - Key accessed - ID: AES_20241017_120530_123456, Algorithm: AES
2024-10-17 12:05:40 - INFO - Data encrypted - Algorithm: AES, User: admin
2024-10-17 12:05:45 - INFO - Data decrypted - Algorithm: AES, User: admin
```

### 8.3 Database Audit Logs

**AuditLog jadvali:**

```python
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))  # ENCRYPT, DECRYPT, ANALYSIS
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    timestamp = db.Column(db.DateTime)
```

**Loglanuvchi hodisalar:**

1. ✅ Foydalanuvchi login/logout
2. ✅ Tahlil bajarish
3. ✅ Ma'lumot shifrlash
4. ✅ Ma'lumot deshifrlash
5. ✅ Kalit yaratish/o'chirish
6. ✅ PDF eksport

---

## 🗺️ 9. TO'LIQ MA'LUMOT OQIMI

### 9.1 Shifrlash Oqimi

```
User Input (Plaintext)
        ↓
Flask Application
        ↓
Analyzer (Algorithm selection)
        ↓
Encryption Module (AES/DES/etc.)
        ↓
Performance Monitoring
        ↓
Key Manager (Key creation)
        ↓
Key Vault (Encrypted storage)
        ↓
EncryptedData Model
        ↓
Database Master Key Encryption
        ↓
SQLite Database (encrypted_data table)
        ↓
Audit Log (File + Database)
```

### 9.2 Deshifrlash Oqimi

```
User Request (encrypted_id)
        ↓
Flask Application
        ↓
Database Query (EncryptedData)
        ↓
Access Control Check
        ↓
Key Manager (Get key)
        ↓
Key Vault (Decrypt vault)
        ↓
Database Master Key Decryption
        ↓
Original Plaintext
        ↓
Return to User
        ↓
Audit Log
```

---

## 📊 10. SAQLASH STATISTIKASI

### 10.1 Hajm Tahlili

**50 bayt matn uchun:**

| Komponent | Hajm | Tavsif |
|-----------|------|--------|
| Original plaintext | 50 bayt | Asl matn |
| Padded plaintext | 64 bayt | PKCS7 padding |
| Ciphertext | 64 bayt | Shifrlangan |
| IV | 16 bayt | Initialization Vector |
| Total binary | 80 bayt | IV + Ciphertext |
| Base64 encoded | ~107 bayt | Database uchun |
| Database overhead | ~50 bayt | Metadata |
| **Total per record** | **~157 bayt** | Jami |

### 10.2 Database Hajmi

**1000 ta shifrlangan matn uchun:**

```
EncryptedData: 1000 × 157 bayt = 157 KB
AnalysisResult: 1000 × 4 × 200 bayt = 800 KB (4 algoritm)
AuditLog: 1000 × 100 bayt = 100 KB
Users: 10 × 500 bayt = 5 KB
-----------------------------------------
Total: ~1.06 MB
```

---

## 🔒 11. XAVFSIZLIK CHORALARI

### 11.1 Defense in Depth

**Qatlam 1: Application Level**
- ✅ Flask session encryption
- ✅ CSRF protection
- ✅ Input validation
- ✅ SQL injection prevention (ORM)

**Qatlam 2: Data Level**
- ✅ Database master key encryption
- ✅ Password hashing (PBKDF2)
- ✅ Key vault encryption
- ✅ Sensitive data not in logs

**Qatlam 3: Access Control**
- ✅ User authentication
- ✅ Ownership verification
- ✅ Role-based access (future)
- ✅ Audit logging

**Qatlam 4: File System**
- ✅ `.gitignore` for sensitive files
- ✅ File permissions
- ✅ Encrypted storage
- ✅ No plaintext on disk

### 11.2 OWASP Top 10 Compliance

| OWASP Risk | Himoya | Status |
|------------|--------|--------|
| A01: Broken Access Control | User ownership check | ✅ |
| A02: Cryptographic Failures | AES-256, proper key mgmt | ✅ |
| A03: Injection | SQLAlchemy ORM | ✅ |
| A04: Insecure Design | Defense in depth | ✅ |
| A05: Security Misconfiguration | Secure defaults | ✅ |
| A06: Vulnerable Components | Updated libraries | ✅ |
| A07: Auth Failures | PBKDF2, session mgmt | ✅ |
| A08: Data Integrity Failures | Integrity checks | ✅ |
| A09: Logging Failures | Comprehensive audit | ✅ |
| A10: SSRF | Input validation | ✅ |

---

## 📋 12. XULOSA

### 12.1 Saqlash Joylari

| Ma'lumot | Joy | Format | Shifrlangan |
|----------|-----|--------|-------------|
| Shifrlangan matn | `encryption_audit.db` | Base64 | ✅ Ha |
| Tahlil natijalari | `encryption_audit.db` | SQL | ❌ Yo'q |
| Kalitlar | `database/key_vault.enc` | Binary | ✅ Ha |
| Master key | `database/.master_key` | Binary | ❌ Yo'q |
| Audit logs | `logs/audit.log` | Text | ❌ Yo'q |
| Session data | Server memory | JSON | ✅ Ha |
| Uploaded files | `uploads/` (temp) | Binary | ❌ Yo'q |

### 12.2 Asosiy Xususiyatlar

1. ✅ **Ikki qatlamli shifrlash:** Algoritm + Database master key
2. ✅ **Markazlashtirilgan saqlash:** Barcha ma'lumot database da
3. ✅ **Xavfsiz kalit boshqaruv:** Encrypted key vault
4. ✅ **To'liq audit:** Barcha amallar loglanadi
5. ✅ **Access control:** Faqat egasi kirishi mumkin
6. ✅ **Defense in depth:** Ko'p qatlamli himoya

### 12.3 Best Practices

- ✅ Plaintext hech qachon disk ga yozilmaydi
- ✅ Kalitlar alohida shifrlangan vault da
- ✅ Database dump ham xavfsiz (shifrlangan)
- ✅ Audit trail barcha amallar uchun
- ✅ User isolation (har bir foydalanuvchi faqat o'z ma'lumotini ko'radi)

**Keyingi qism:** Web interfeys, frontend texnologiyalari va deployment strategiyasi
