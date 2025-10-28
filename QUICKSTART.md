# ⚡ Tezkor Boshlash Qo'llanmasi

## 🎯 3 Qadamda Ishga Tushiring

### Windows Foydalanuvchilari:

1. **`run.bat` faylini ikki marta bosing**
   - Avtomatik ravishda virtual muhit yaratiladi
   - Kutubxonalar o'rnatiladi
   - Ma'lumotlar bazasi yaratiladi
   - Server ishga tushadi

2. **Brauzerda oching:**
   ```
   http://localhost:5000
   ```

3. **Kirish:**
   - Username: `admin`
   - Password: `admin123`

### Linux/macOS Foydalanuvchilari:

```bash
chmod +x run.sh
./run.sh
```

## 📱 Qisqa Yo'riqnoma

### 1️⃣ Dashboard
- Asosiy sahifa
- Statistika va tezkor havolalar
- So'nggi tahlillar

### 2️⃣ Tahlil Sahifasi
1. "Tahlil" menyusiga o'ting
2. Matn kiriting yoki fayl yuklang
3. "Tahlilni Boshlash" tugmasini bosing
4. Natijalarni ko'ring:
   - Bar chart (umumiy ball)
   - Radar chart (ko'rsatkichlar)
   - Performance chart (CPU/RAM)
   - Batafsil jadval

### 3️⃣ Hisobot
1. "Hisobot" menyusiga o'ting
2. Oxirgi tahlil natijalarini ko'ring
3. "PDF Eksport" tugmasi bilan yuklab oling

### 4️⃣ Tarix
- Barcha o'tgan tahlillarni ko'rish
- Vaqt bo'yicha saralash

## 🔐 Xavfsizlik Xususiyatlari

✅ **Shifrlangan ma'lumotlar bazasi** - Barcha maxfiy ma'lumotlar AES bilan shifrlangan
✅ **Kalit boshqaruv** - Avtomatik kalit yaratish va rotatsiya
✅ **Audit log** - Barcha harakatlar qayd etiladi
✅ **Hash parollar** - Parollar xavfsiz hash qilingan

## 📊 Qo'llab-quvvatlanadigan Algoritmlar

| Algoritm | Kalit Hajmi | Xavfsizlik | Tezlik |
|----------|-------------|------------|--------|
| **AES** | 256-bit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **ChaCha20** | 256-bit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Blowfish** | 128-bit | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **DES** | 56-bit | ⭐ | ⭐⭐⭐ |

## 🎨 Interfeys Xususiyatlari

- 🌓 **Dark/Light Mode** - Tema o'zgartirish
- 📱 **Responsive Design** - Barcha qurilmalarda ishlaydi
- 📊 **Interaktiv Grafiklar** - Chart.js bilan
- 🎯 **Zamonaviy UI** - TailwindCSS dizayni

## 🚀 Tezkor Maslahatlar

1. **Katta fayllar uchun:** Maksimal 16MB
2. **Eng yaxshi natija:** AES yoki ChaCha20 tavsiya etiladi
3. **Tahlil vaqti:** 1-5 soniya (ma'lumot hajmiga bog'liq)
4. **PDF eksport:** Hisobot sahifasidan

## ❓ Tez-tez So'raladigan Savollar

**S: Server ishga tushmayapti?**
J: `pip install -r requirements.txt` buyrug'ini bajaring

**S: PDF eksport ishlamayapti?**
J: WeasyPrint kutubxonasi to'g'ri o'rnatilganligini tekshiring

**S: Parolni unutdim?**
J: Ma'lumotlar bazasini qayta yarating: `python database/db_init.py`

**S: Portni o'zgartirish kerakmi?**
J: `app.py` faylida `port=5000` ni o'zgartiring

## 📞 Yordam

Muammolar yuzaga kelsa:
- `logs/audit.log` faylini tekshiring
- `INSTALL.md` faylini o'qing
- Terminal xatoliklarini diqqat bilan o'qing

---

**Omad! Samarali tahlillar! 🎉**
