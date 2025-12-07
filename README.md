# 🧠 Intellektual Audit Modeli - Dasturiy Ta'minot Xavfsizligi Tahlil Tizimi

## Loyiha haqida
Bu veb-ilova simmetrik shifrlash algoritmlarini (AES, DES, Blowfish, ChaCha20) tahlil qilish va ularning samaradorligini baholash uchun mo'ljallangan.

## Asosiy imkoniyatlar
- ✅ Matn va fayllarni shifrlash/deshifrlash
- ✅ Algoritmlar samaradorligini tahlil qilish
- ✅ Xavfsizlik kalit boshqaruv tizimi
- ✅ Interaktiv grafiklar va vizualizatsiya
- ✅ PDF hisobot generatsiyasi
- ✅ Zamonaviy responsive dizayn
- ✅ Dark/Light theme qo'llab-quvvatlash

## O'rnatish

### 1. Virtual muhit yaratish
```bash
git clone git@github.com:MuxammadiyevG/Compare_Algorithm.git
```
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Kerakli kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini yaratish
```bash
python -c "from database.db_init import init_db; init_db()"
```

### 4. Ilovani ishga tushirish
```bash
python app.py
```

Brauzerda `http://localhost:5000` manziliga o'ting.

## Standart foydalanuvchi
- **Username:** admin
- **Password:** admin123

## Texnologiyalar
- **Backend:** Flask, SQLAlchemy
- **Security:** cryptography, pycryptodome
- **Frontend:** TailwindCSS, Chart.js
- **Analysis:** psutil, matplotlib
- **Export:** WeasyPrint, reportlab

## Loyiha strukturasi
```
project_root/
├── app.py                 # Asosiy Flask ilovasi
├── config.py              # Konfiguratsiya
├── requirements.txt       # Python kutubxonalari
├── modules/               # Backend modullar
├── templates/             # HTML shablonlar
├── static/                # CSS, JS, rasmlar
├── database/              # Ma'lumotlar bazasi
└── logs/                  # Audit loglar
```

## Litsenziya
MIT License
