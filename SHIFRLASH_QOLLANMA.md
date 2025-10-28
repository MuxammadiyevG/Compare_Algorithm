# 🔐 Shifrlangan Ma'lumotlar Qo'llanmasi

## 📋 Umumiy Ma'lumot

Bu qo'llanma sizga fayl yoki matnni qanday shifrlash, saqlash va deshifrlash haqida to'liq ma'lumot beradi.

---

## 🎯 1. FAYL/MATN SHIFRLASH VA SAQLASH

### Qadam 1: Tahlil Sahifasiga O'tish

1. Tizimga kiring (login: `admin`, parol: `admin123`)
2. Yuqori menyudan **"Tahlil"** tugmasini bosing
3. Yoki: `http://localhost:5000/analyze` ga o'ting

### Qadam 2: Ma'lumot Kiritish

**Variant A: Matn kiritish**
```
1. "Matn" radio tugmasini tanlang
2. Textarea ga matn kiriting
3. "Tahlilni Boshlash" tugmasini bosing
```

**Variant B: Fayl yuklash**
```
1. "Fayl" radio tugmasini tanlang
2. "Fayl yuklash" tugmasini bosing
3. Faylni tanlang (har qanday matn fayl)
4. "Tahlilni Boshlash" tugmasini bosing
```

### Qadam 3: Tahlil Kutish

- Loading animatsiya ko'rsatiladi
- Progress bar to'ladi
- 4 ta algoritm tahlil qilinadi:
  - ✅ AES-256
  - ✅ ChaCha20
  - ✅ Blowfish
  - ⚠️ DES (zaif)

### Qadam 4: Ma'lumotni Saqlash

Tahlil tugagandan keyin:

1. **"Saqlash"** tugmasini bosing (yashil tugma)
2. Modal oyna ochiladi
3. Shifrlash algoritmini tanlang:
   - **AES-256** (Tavsiya etiladi) ⭐
   - **ChaCha20** (Zamonaviy)
   - **Blowfish** (O'rtacha)
   - **DES** (Zaif - tavsiya etilmaydi) ❌

4. **"Saqlash"** tugmasini bosing
5. Muvaffaqiyat xabari ko'rsatiladi
6. "Shifrlangan ma'lumotlarni ko'rmoqchimisiz?" - **Ha** tugmasini bosing

---

## 🔓 2. SHIFRLANGAN MA'LUMOTLARNI KO'RISH

### Usul 1: Tahlildan keyin

Tahlil tugagandan keyin "Saqlash" bosganda avtomatik yo'naltiriladi.

### Usul 2: Menyu orqali

1. Yuqori menyudan **"Shifrlangan"** tugmasini bosing
2. Yoki: `http://localhost:5000/encrypted` ga o'ting

### Nima ko'rasiz?

Har bir shifrlangan ma'lumot uchun:

```
┌─────────────────────────────────────────┐
│ 🔒 Shifrlangan Matn #1                  │
│                                         │
│ Algoritm: AES-256                       │
│ Turi: Matn                              │
│ Kalit ID: AES_20241017_120530...        │
│ Status: Xavfsiz                         │
│                                         │
│ [Deshifrlash] [O'chirish]               │
└─────────────────────────────────────────┘
```

---

## 🔓 3. MA'LUMOTNI DESHIFRLASH

### Qadam 1: Deshifrlash Tugmasini Bosish

1. Shifrlangan ma'lumotlar sahifasida
2. Kerakli ma'lumotni toping
3. **"Deshifrlash"** tugmasini bosing (yashil tugma)

### Qadam 2: Natijani Ko'rish

Modal oyna ochiladi va ko'rsatiladi:

```
┌─────────────────────────────────────────┐
│ 🔓 Deshifrlangan Ma'lumot               │
│                                         │
│ Algoritm: AES-256                       │
│ ✅ Deshifrlash muvaffaqiyatli!          │
│                                         │
│ Asl Matn:                               │
│ ┌─────────────────────────────────────┐ │
│ │ Bu test matni. Shifrlash            │ │
│ │ algoritmlari tahlil qilinmoqda.     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [Nusxa Olish] [Yopish]                  │
└─────────────────────────────────────────┘
```

### Qadam 3: Nusxa Olish (ixtiyoriy)

1. **"Nusxa Olish"** tugmasini bosing
2. Matn clipboard ga ko'chiriladi
3. Istalgan joyga paste qiling (Ctrl+V)

---

## 🗑️ 4. SHIFRLANGAN MA'LUMOTNI O'CHIRISH

### Ehtiyot bo'ling! ⚠️

O'chirilgan ma'lumotni qayta tiklab bo'lmaydi!

### Qadamlar:

1. Shifrlangan ma'lumotlar sahifasida
2. O'chirmoqchi bo'lgan ma'lumotni toping
3. **"O'chirish"** tugmasini bosing (qizil tugma)
4. Tasdiqlash oynasi: **"Ha"** tugmasini bosing
5. Ma'lumot o'chiriladi

---

## 📊 5. MA'LUMOTLAR QAYERDA SAQLANADI?

### Database (Asosiy Saqlash)

**Fayl:** `encryption_audit.db`  
**Jadval:** `encrypted_data`

```sql
CREATE TABLE encrypted_data (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    algorithm VARCHAR(50),
    encrypted_content TEXT,      -- Shifrlangan (Base64)
    key_id VARCHAR(100),
    original_filename VARCHAR(255),
    content_type VARCHAR(50),
    created_at DATETIME
);
```

### Shifrlash Jarayoni

```
Original Text/File
      ↓
[Tanlangan Algoritm bilan shifrlash]
      ↓
[Database Master Key bilan qayta shifrlash]
      ↓
[Base64 encoding]
      ↓
Database (encrypted_content ustuni)
```

### Kalitlar

**Fayl:** `database/key_vault.enc`

Barcha shifrlash kalitlari shifrlangan vault da saqlanadi:
- AES kalitlari
- ChaCha20 kalitlari
- Blowfish kalitlari
- IV/Nonce qiymatlari

---

## 🔒 6. XAVFSIZLIK

### Ikki Qatlamli Shifrlash

1. **Birinchi qatlam:** Siz tanlagan algoritm (AES/ChaCha20/etc.)
2. **Ikkinchi qatlam:** Database master key (AES-256)

### Faqat Siz Ko'rasiz

- Har bir foydalanuvchi faqat o'z ma'lumotlarini ko'radi
- Boshqa foydalanuvchilar sizning ma'lumotlaringizni ko'ra olmaydi
- Admin ham sizning ma'lumotlaringizni deshifrlay olmaydi (kalit yo'q)

### Audit Log

Barcha amallar loglanadi:
- Qachon shifrlangan
- Qachon deshifrlangan
- Qachon o'chirilgan
- Qaysi IP manzildan

---

## 💡 7. MASLAHATLAR

### Qaysi Algoritmni Tanlash?

| Algoritm | Xavfsizlik | Tezlik | Tavsiya |
|----------|------------|--------|---------|
| **AES-256** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Eng yaxshi |
| **ChaCha20** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Mobil uchun |
| **Blowfish** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⚠️ Legacy |
| **DES** | ⭐ | ⭐⭐⭐⭐⭐ | ❌ Ishlatmang! |

### Muhim Ma'lumotlar Uchun

1. ✅ **AES-256** yoki **ChaCha20** ishlatish
2. ✅ Kalit ID ni eslab qolish
3. ✅ Backup olish (database)
4. ❌ DES ishlatmaslik

### Katta Fayllar Uchun

- Maksimal hajm: **16 MB**
- Tavsiya: **< 5 MB**
- Katta fayllar uchun: Zip qilib yuklang

---

## 🐛 8. MUAMMOLAR VA YECHIMLAR

### Muammo 1: "Ma'lumot topilmadi"

**Sabab:** Tahlil bajarilmagan  
**Yechim:** Avval tahlil bajaring, keyin saqlang

### Muammo 2: "Ruxsat yo'q"

**Sabab:** Boshqa foydalanuvchining ma'lumoti  
**Yechim:** Faqat o'z ma'lumotlaringizni deshifrlang

### Muammo 3: "Kalit topilmadi"

**Sabab:** Key vault buzilgan yoki o'chirilgan  
**Yechim:** Database backup dan tiklang

### Muammo 4: Deshifrlash xatosi

**Sabab:** Database yoki kalit buzilgan  
**Yechim:** 
1. Database integrity tekshiring
2. Backup dan tiklang
3. Yangi ma'lumot yarating

---

## 📱 9. FOYDALANISH MISOLI

### Misol: Maxfiy Xabarni Saqlash

```
1. Login qiling
2. "Tahlil" sahifasiga o'ting
3. "Matn" ni tanlang
4. Xabarni kiriting: "Bu maxfiy xabar"
5. "Tahlilni Boshlash" ni bosing
6. Kutish (5-10 soniya)
7. "Saqlash" tugmasini bosing
8. "AES-256" ni tanlang
9. "Saqlash" ni bosing
10. "Ha" ni bosing (shifrlangan sahifaga o'tish)
11. Xabaringiz shifrlangan holda ko'rsatiladi
```

### Misol: Xabarni O'qish

```
1. "Shifrlangan" sahifasiga o'ting
2. Kerakli xabarni toping
3. "Deshifrlash" tugmasini bosing
4. Modal oynada asl xabarni ko'ring
5. "Nusxa Olish" ni bosing (kerak bo'lsa)
6. "Yopish" ni bosing
```

---

## 🎓 10. TEXNIK TAFSILOTLAR

### Shifrlash Parametrlari

**AES-256:**
```
Kalit hajmi: 256-bit (32 bayt)
IV hajmi: 128-bit (16 bayt)
Rejim: CBC
Padding: PKCS7
```

**ChaCha20:**
```
Kalit hajmi: 256-bit (32 bayt)
Nonce hajmi: 128-bit (16 bayt)
Rejim: Stream cipher
Padding: Kerak emas
```

### Database Saqlash Formati

```
encrypted_content = Base64(IV + AES-256-CBC(plaintext))
```

Misol:
```
Original: "Hello World"
↓
Padding: "Hello World\x05\x05\x05\x05\x05"
↓
AES-256 encrypt: [binary data]
↓
IV + Ciphertext: [16 bytes IV][encrypted data]
↓
Base64: "SGVsbG8gV29ybGQh..."
↓
Database: TEXT column
```

---

## 📞 11. YORDAM

### Qo'shimcha Ma'lumot

- **README.md** - Loyiha haqida
- **QUICKSTART.md** - Tez boshlash
- **HISOBOT_*.md** - Texnik hisobotlar

### Muammo Bo'lsa

1. Audit loglarni tekshiring: `logs/audit.log`
2. Database ni tekshiring: `encryption_audit.db`
3. Key vault ni tekshiring: `database/key_vault.enc`

---

## ✅ XULOSA

Endi siz:
- ✅ Matn/faylni shifrlashni bilasiz
- ✅ Shifrlangan ma'lumotlarni ko'rishni bilasiz
- ✅ Ma'lumotni deshifrlashni bilasiz
- ✅ Xavfsiz saqlashni bilasiz

**Esda tuting:**
- 🔐 Har doim kuchli algoritm (AES-256, ChaCha20) ishlatish
- 💾 Muntazam backup olish
- 🔒 Kalit ID ni eslab qolish
- ❌ DES ishlatmaslik

**Omad tilaymiz! 🚀**
