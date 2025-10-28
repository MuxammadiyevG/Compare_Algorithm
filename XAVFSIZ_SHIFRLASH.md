# 🔐 Xavfsiz Shifrlash Tizimi

## 📋 Umumiy Ma'lumot

Bu tizim fayllarni **xotirada (in-memory)** shifrlash va deshifrlash imkonini beradi. Hech qanday vaqtinchalik fayl diskda saqlanmaydi, bu esa maksimal xavfsizlikni ta'minlaydi.

## 🔑 Asosiy Konsepsiya

### MASTER_KEY
- Tizimda o'zgarmas **256-bit AES kalit**
- `.env` faylda saqlanadi va **hech qachon o'zgartirilmaydi**
- Faqat session kalitlarini shifrlash uchun ishlatiladi
- Foydalanuvchi ma'lumotlarini to'g'ridan-to'g'ri shifrlash uchun ishlatilmaydi

### Session Key (Sessiya Kaliti)
- Har bir fayl uchun **yangi tasodifiy kalit** yaratiladi
- Faylni shifrlash uchun ishlatiladi
- MASTER_KEY bilan o'raladi (key wrapping)
- Foydalanuvchiga `.key` fayl sifatida beriladi

## ⚙️ Shifrlash Jarayoni

```
1. Foydalanuvchi fayl yuklaydi
   ↓
2. Tizim tasodifiy session_key yaratadi (32-byte)
   ↓
3. Fayl session_key bilan RAM ichida shiflanadi
   ↓
4. session_key MASTER_KEY bilan shiflanadi (key wrapping)
   ↓
5. Foydalanuvchiga 2 ta fayl qaytariladi:
   - encrypted_data.enc (shifrlangan fayl)
   - encrypted_key.bin (shifrlangan session_key)
   ↓
6. Hech narsa serverda saqlanmaydi ✓
```

## 🔓 Deshifrlash Jarayoni

```
1. Foydalanuvchi 2 ta faylni yuklaydi:
   - encrypted_data.enc
   - encrypted_key.bin
   ↓
2. Tizim encrypted_key.bin ni MASTER_KEY bilan ochadi
   ↓
3. Session_key olinadi
   ↓
4. encrypted_data.enc session_key bilan RAM ichida deshiflanadi
   ↓
5. Asl fayl foydalanuvchiga qaytariladi
   ↓
6. Hech narsa serverda saqlanmaydi ✓
```

## 🚀 O'rnatish va Ishga Tushirish

### 1. Muhitni Tayyorlash

```bash
# Virtual muhit yaratish
python -m venv venv

# Virtual muhitni faollashtirish
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt
```

### 2. .env Faylni Yaratish

```bash
# Setup skriptini ishga tushirish
python setup_env.py
```

Bu skript avtomatik ravishda:
- ✅ Xavfsiz MASTER_KEY yaratadi (256-bit)
- ✅ Flask SECRET_KEY yaratadi
- ✅ `.env` faylni yaratadi

**MUHIM:** `.env` faylni zaxira nusxasini oling va xavfsiz joyda saqlang!

### 3. Dasturni Ishga Tushirish

```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

Brauzerda ochish: `http://localhost:6001`

## 🎯 Qo'llanilishi

### Shifrlash

1. **Shifrlash** sahifasiga o'ting
2. Algoritmni tanlang:
   - **AES-256**: Yuqori xavfsizlik, tez ishlash (tavsiya etiladi)
   - **Fernet**: AES + HMAC, yuqori yaxlitlik
   - **ChaCha20**: Zamonaviy, juda tez
3. Faylni yuklang (maksimal 16 MB)
4. **Shifrlash** tugmasini bosing
5. 2 ta faylni yuklab oling:
   - `filename.enc` - shifrlangan fayl
   - `filename.key` - shifrlangan kalit

### Deshifrlash

1. **Deshifrlash** sahifasiga o'ting
2. Shifrlashda ishlatilgan algoritmni tanlang
3. Ikkala faylni yuklang:
   - `.enc` fayl
   - `.key` fayl
4. **Deshifrlash** tugmasini bosing
5. Asl faylni yuklab oling

## 🔒 Xavfsizlik Xususiyatlari

### ✅ Afzalliklar

1. **In-Memory Processing**
   - Hech qanday vaqtinchalik fayl yaratilmaydi
   - Barcha operatsiyalar RAM ichida bajariladi
   - Disk I/O xavfi yo'q

2. **Key Wrapping**
   - Session kalitlar MASTER_KEY bilan himoyalangan
   - Har bir fayl uchun yangi kalit
   - Forward secrecy ta'minlanadi

3. **Zero Persistence**
   - Serverda hech narsa saqlanmaydi
   - Session tugagach barcha ma'lumotlar o'chiriladi
   - Audit log faqat metama'lumotlarni saqlaydi

4. **Multiple Algorithms**
   - AES-256-CBC
   - Fernet (AES-128-CBC + HMAC-SHA256)
   - ChaCha20

### ⚠️ Muhim Ogohlantirishlar

1. **MASTER_KEY ni o'zgartirmang**
   - Agar o'zgartirsangiz, eski shifrlangan fayllar ochilmaydi
   - Zaxira nusxasini xavfsiz joyda saqlang

2. **Ikkala faylni ham saqlang**
   - `.enc` va `.key` fayllar ikkalasi ham kerak
   - Bittasini yo'qotsangiz, faylni tiklab bo'lmaydi

3. **Algoritmni eslang**
   - Deshifrlashda xuddi shu algoritmni tanlang
   - Noto'g'ri algoritm xatolikka olib keladi

4. **Fayl hajmi cheklovi**
   - Maksimal 16 MB (Flask konfiguratsiyasi)
   - Katta fayllar uchun chunked upload kerak

## 📊 Qo'llab-quvvatlanadigan Algoritmlar

| Algoritm | Kalit Hajmi | Xavfsizlik | Tezlik | Tavsiya |
|----------|-------------|------------|--------|---------|
| AES-256  | 256-bit     | Yuqori     | Tez    | ⭐⭐⭐ |
| Fernet   | 128-bit     | Yuqori     | O'rta  | ⭐⭐   |
| ChaCha20 | 256-bit     | Yuqori     | Juda tez | ⭐⭐⭐ |

## 🛠️ Texnik Tafsilotlar

### Arxitektura

```
┌─────────────────────────────────────────────────────────┐
│                    Foydalanuvchi                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Flask Web Server                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │           MemoryEncryptor Module                 │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │  1. Generate random session_key           │  │  │
│  │  │  2. Encrypt file with session_key (RAM)   │  │  │
│  │  │  3. Wrap session_key with MASTER_KEY      │  │  │
│  │  │  4. Return BytesIO streams                │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              .env (MASTER_KEY)                          │
│              [Hech qachon o'zgartirilmaydi]             │
└─────────────────────────────────────────────────────────┘
```

### Kod Misoli

```python
from modules.memory_encryptor import MemoryEncryptor
from io import BytesIO

# Initialize
encryptor = MemoryEncryptor(master_key_b64)

# Encrypt
file_stream = BytesIO(file_data)
encrypted_data, encrypted_key = encryptor.encrypt_file_aes(file_stream)

# Decrypt
decrypted_data = encryptor.decrypt_file_aes(encrypted_data, encrypted_key)
```

## 📝 API Endpoints

### POST /secure-encrypt
Faylni shifrlash

**Request:**
- `algorithm`: AES, Fernet, yoki ChaCha20
- `file`: Yuklash uchun fayl

**Response:**
```json
{
  "success": true,
  "message": "Fayl muvaffaqiyatli shifrlandi!",
  "algorithm": "AES",
  "filename": "document.pdf"
}
```

### GET /download-encrypted-data
Shifrlangan faylni yuklab olish

### GET /download-encrypted-key
Shifrlangan kalitni yuklab olish

### POST /secure-decrypt
Faylni deshifrlash

**Request:**
- `algorithm`: AES, Fernet, yoki ChaCha20
- `encrypted_file`: .enc fayl
- `key_file`: .key fayl

**Response:**
```json
{
  "success": true,
  "message": "Fayl muvaffaqiyatli deshifrlandi!",
  "algorithm": "AES"
}
```

### GET /download-decrypted
Deshifrlangan faylni yuklab olish

## 🔍 Audit Log

Barcha shifrlash/deshifrlash operatsiyalari audit logga yoziladi:

```
[2024-01-15 10:30:45] USER: admin | ACTION: SECURE_ENCRYPT | DETAILS: Encrypted file document.pdf with AES (in-memory)
[2024-01-15 10:35:12] USER: admin | ACTION: SECURE_DECRYPT | DETAILS: Decrypted file with AES (in-memory)
```

## 🆘 Muammolarni Hal Qilish

### MASTER_KEY topilmadi
```
Error: MASTER_KEY not configured in .env file!
```
**Yechim:** `python setup_env.py` ni ishga tushiring

### Deshifrlash xatosi
```
Error: Decryption failed
```
**Yechim:**
- To'g'ri algoritmni tanlaganingizni tekshiring
- To'g'ri `.enc` va `.key` fayllarni yuklayotganingizni tekshiring
- Fayllar buzilmaganligini tekshiring

### Fayl hajmi xatosi
```
Error: File too large
```
**Yechim:** Fayl hajmi 16 MB dan kichik bo'lishi kerak

## 📚 Qo'shimcha Resurslar

- [AES Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [Fernet Specification](https://github.com/fernet/spec/)
- [ChaCha20 Algorithm](https://en.wikipedia.org/wiki/Salsa20#ChaCha_variant)
- [Key Wrapping](https://en.wikipedia.org/wiki/Key_wrap)

## 📄 Litsenziya

Bu loyiha ta'lim maqsadida yaratilgan.

## 👨‍💻 Muallif

Intellektual Audit Modeli - Dasturiy Ta'minot Xavfsizligi Tahlil Tizimi

---

**Eslatma:** Bu tizim production muhitida ishlatishdan oldin qo'shimcha xavfsizlik tekshiruvlaridan o'tkazilishi kerak.
