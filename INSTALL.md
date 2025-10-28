# 🚀 O'rnatish va Ishga Tushirish Qo'llanmasi

## Tizim Talablari

- **Python:** 3.8 yoki yuqori versiya
- **RAM:** Minimal 2GB
- **Disk:** 500MB bo'sh joy
- **OS:** Windows, Linux, macOS

## 1️⃣ Loyihani Yuklab Olish

Loyiha fayllarini `New folder` papkasiga joylashtiring.

## 2️⃣ Virtual Muhit Yaratish

### Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Kutubxonalarni O'rnatish

```bash
pip install -r requirements.txt
```

### Agar xatolik yuz bersa:

**Windows uchun:**
```powershell
pip install --upgrade pip
pip install Flask==3.0.0
pip install Flask-Login==0.6.3
pip install Flask-SQLAlchemy==3.1.1
pip install cryptography==41.0.7
pip install pycryptodome==3.19.0
pip install psutil==5.9.6
pip install matplotlib==3.8.2
pip install reportlab==4.0.7
pip install WeasyPrint==60.1
pip install Werkzeug==3.0.1
pip install python-dotenv==1.0.0
```

**WeasyPrint uchun qo'shimcha:**
Windows'da WeasyPrint ishlashi uchun GTK3 kerak bo'lishi mumkin:
- https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases dan yuklab oling

## 4️⃣ Ma'lumotlar Bazasini Yaratish

```bash
python database/db_init.py
```

Yoki:
```bash
python -c "from database.db_init import init_db; init_db()"
```

## 5️⃣ Ilovani Ishga Tushirish

```bash
python app.py
```

Muvaffaqiyatli ishga tushgandan keyin quyidagi xabar ko'rinadi:
```
============================================================
🧠 Intellektual Audit Modeli - Dasturiy Ta'minot Xavfsizligi
============================================================
✓ Server ishga tushmoqda...
✓ Brauzerda quyidagi manzilga o'ting: http://localhost:5000
✓ Standart foydalanuvchi: admin / admin123
============================================================
```

## 6️⃣ Brauzerda Ochish

Brauzeringizda quyidagi manzilga o'ting:
```
http://localhost:5000
```

## 🔐 Kirish Ma'lumotlari

**Standart foydalanuvchi:**
- **Username:** admin
- **Password:** admin123

## 📁 Loyiha Strukturasi

```
New folder/
├── app.py                      # Asosiy Flask ilovasi
├── config.py                   # Konfiguratsiya
├── requirements.txt            # Python kutubxonalari
├── README.md                   # Loyiha haqida
├── INSTALL.md                  # O'rnatish qo'llanmasi
│
├── modules/                    # Backend modullar
│   ├── encryption/            # Shifrlash algoritmlari
│   │   ├── aes.py
│   │   ├── des.py
│   │   ├── blowfish.py
│   │   └── chacha20.py
│   ├── key_manager.py         # Kalit boshqaruv
│   ├── analyzer.py            # Tahlil moduli
│   └── report_generator.py    # Hisobot yaratish
│
├── database/                   # Ma'lumotlar bazasi
│   ├── models.py              # DB modellari
│   └── db_init.py             # DB yaratish
│
├── templates/                  # HTML shablonlar
│   ├── base.html
│   ├── login.html
│   ├── index.html
│   ├── analyze.html
│   ├── report.html
│   └── history.html
│
├── static/                     # Statik fayllar
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── charts.js
│   └── img/
│
├── logs/                       # Audit loglar
├── uploads/                    # Yuklangan fayllar
└── encryption_audit.db        # SQLite bazasi (avtomatik yaratiladi)
```

## 🔧 Muammolarni Hal Qilish

### 1. ModuleNotFoundError
```bash
pip install --upgrade -r requirements.txt
```

### 2. WeasyPrint xatoligi (Windows)
GTK3 o'rnatilganligiga ishonch hosil qiling yoki PDF eksport funksiyasini vaqtincha o'chiring.

### 3. Port band
Agar 5000-port band bo'lsa, `app.py` faylida portni o'zgartiring:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 4. Database xatoligi
Ma'lumotlar bazasini qayta yarating:
```bash
rm encryption_audit.db
python database/db_init.py
```

## 🎯 Asosiy Funksiyalar

### ✅ Shifrlash va Tahlil
1. Dashboard sahifasidan "Yangi Tahlil" tugmasini bosing
2. Matn yoki fayl kiriting
3. "Tahlilni Boshlash" tugmasini bosing
4. Natijalarni ko'ring va taqqoslang

### ✅ Hisobot Yaratish
1. Tahlildan keyin "Hisobot" sahifasiga o'ting
2. Natijalarni ko'ring
3. "PDF Eksport" tugmasini bosing

### ✅ Tarix
Barcha o'tgan tahlillarni "Tarix" sahifasida ko'ring

## 🔒 Xavfsizlik

- Parollar hash qilingan holda saqlanadi (Werkzeug)
- Ma'lumotlar bazasidagi maxfiy ma'lumotlar AES bilan shifrlangan
- Kalitlar shifrlangan vault'da saqlanadi
- Barcha harakatlar audit log'da qayd etiladi

## 📊 Tahlil Ko'rsatkichlari

Har bir algoritm uchun quyidagi ko'rsatkichlar hisoblanadi:

- **T (Performance):** Tezlik va resurs sarfi
- **E (Security):** Xavfsizlik darajasi
- **K (Key Management):** Kalit boshqaruv samaradorligi
- **I (Integrity):** Yaxlitlik va ishonchlilik
- **S (Overall Score):** Umumiy samaradorlik balli

**Formula:** S = 0.25·T + 0.35·E + 0.25·K + 0.15·I

## 🌐 Tarmoqda Ishlatish

Ilovani tarmoqda ishlatish uchun:

```bash
python app.py
```

Keyin boshqa kompyuterlardan quyidagi manzilga kiring:
```
http://[SERVER_IP]:5000
```

## 🛠️ Ishlab Chiqish Rejimi

Debug rejimini o'chirish uchun `app.py` faylida:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## 📝 Litsenziya

MIT License - Bepul foydalanish va o'zgartirish mumkin.

## 🤝 Yordam

Muammolar yuzaga kelsa:
1. `logs/audit.log` faylini tekshiring
2. Terminal/CMD'dagi xatolik xabarlarini o'qing
3. Barcha kutubxonalar to'g'ri o'rnatilganligini tekshiring

---

**Muvaffaqiyatli ishlashni tilaymiz! 🎉**
