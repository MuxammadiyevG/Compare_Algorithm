# 🧠 Intellektual Audit Modeli - Loyiha Xulosasi

## 📋 Loyiha Nomi
**Intellektual audit modeli asosida dasturiy ta'minot xavfsizligini ta'minlash samaradorligini oshirish uchun simmetrik shifrlash algoritmlari va kalit boshqaruv tizimlarining tahlili**

## 🎯 Loyiha Maqsadi
Simmetrik shifrlash algoritmlarini (AES, DES, Blowfish, ChaCha20) kompleks tahlil qilish va ularning samaradorligini baholash uchun to'liq funksional veb-ilova yaratish.

## ✨ Asosiy Xususiyatlar

### 1. Shifrlash Algoritmlari
- ✅ **AES-256** - Advanced Encryption Standard (CBC mode)
- ✅ **DES** - Data Encryption Standard (CBC mode)
- ✅ **Blowfish-128** - Blowfish Cipher (CBC mode)
- ✅ **ChaCha20** - Modern Stream Cipher

### 2. Tahlil Ko'rsatkichlari
Har bir algoritm uchun quyidagi metrikalar hisoblanadi:

#### Performance Metrics (T)
- Shifrlash vaqti (millisekund)
- Deshifrlash vaqti (millisekund)
- CPU yuklanishi (%)
- RAM sarfi (MB)

#### Security Metrics (E)
- Kalit hajmi (bit)
- Entropiya (Shannon entropy, 0-1)
- Xavfsizlik darajasi (High/Medium/Low)

#### Key Management Metrics (K)
- Kalit boshqaruv samaradorligi
- Kalit rotatsiya qo'llab-quvvatlash
- Kalit saqlash xavfsizligi

#### Integrity Metrics (I)
- Yaxlitlik tekshiruvi
- Ma'lumot izchilligi
- Shifrlash/deshifrlash muvaffaqiyati

### 3. Umumiy Samaradorlik Formulasi
```
S = w₁·T + w₂·E + w₃·K + w₄·I

Bu yerda:
- w₁ = 0.25 (Performance weight)
- w₂ = 0.35 (Security weight)
- w₃ = 0.25 (Key Management weight)
- w₄ = 0.15 (Integrity weight)
```

## 🏗️ Arxitektura

### Backend
- **Framework:** Flask 3.0.0
- **Database:** SQLAlchemy + SQLite
- **Authentication:** Flask-Login
- **Encryption:** cryptography, pycryptodome
- **Performance:** psutil, tracemalloc
- **Reports:** WeasyPrint, reportlab

### Frontend
- **CSS Framework:** TailwindCSS 3.x
- **Charts:** Chart.js 4.4.0
- **Icons:** Font Awesome 6.4.2
- **Interactivity:** Alpine.js 3.x
- **Design:** Modern, Responsive, Dark/Light themes

### Security Features
- ✅ Password hashing (Werkzeug)
- ✅ Database encryption (AES-256)
- ✅ Encrypted key vault
- ✅ Audit logging
- ✅ Session management
- ✅ CSRF protection

## 📊 Vizualizatsiya

### 1. Bar Chart
Algoritmlarning umumiy samaradorlik ballarini taqqoslash

### 2. Radar Chart
To'rt asosiy ko'rsatkichni (T, E, K, I) vizual taqqoslash

### 3. Line Chart
CPU va RAM sarfini taqqoslash

### 4. Batafsil Jadvallar
Barcha metrikalarni raqamli ko'rinishda taqdim etish

## 🎨 UI/UX Xususiyatlari

### Design Principles
- **Minimalizm:** Tozalangan, professional interfeys
- **Responsivlik:** Barcha qurilmalarda ishlaydi
- **Accessibility:** Foydalanuvchiga qulay
- **Performance:** Tez yuklanish va silliq animatsiyalar

### Color Scheme
- **Primary:** Indigo/Purple gradient (#4F46E5, #7C3AED)
- **Success:** Green (#10B981)
- **Warning:** Yellow (#F59E0B)
- **Danger:** Red (#EF4444)
- **Neutral:** Gray shades

### Components
- Glassmorphism effects
- Neumorphism cards
- Smooth transitions
- Loading animations
- Interactive tooltips

## 📁 Fayl Strukturasi

```
New folder/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── INSTALL.md                      # Installation guide
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_SUMMARY.md              # This file
├── .gitignore                      # Git ignore rules
├── run.bat                         # Windows launcher
├── run.sh                          # Linux/macOS launcher
│
├── modules/                        # Backend modules
│   ├── __init__.py
│   ├── encryption/                 # Encryption algorithms
│   │   ├── __init__.py
│   │   ├── aes.py                  # AES implementation
│   │   ├── des.py                  # DES implementation
│   │   ├── blowfish.py             # Blowfish implementation
│   │   └── chacha20.py             # ChaCha20 implementation
│   ├── key_manager.py              # Key management system
│   ├── analyzer.py                 # Analysis engine
│   └── report_generator.py         # PDF report generator
│
├── database/                       # Database layer
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy models
│   └── db_init.py                  # Database initialization
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── login.html                  # Login page
│   ├── index.html                  # Dashboard
│   ├── analyze.html                # Analysis page
│   ├── report.html                 # Report page
│   └── history.html                # History page
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css               # Custom styles
│   ├── js/
│   │   └── charts.js               # Chart utilities
│   └── img/                        # Images
│
├── logs/                           # Audit logs
│   └── audit.log                   # System audit log
│
└── uploads/                        # Uploaded files
```

## 🔒 Xavfsizlik Arxitekturasi

### 1. Foydalanuvchi Autentifikatsiyasi
- Parollar Werkzeug bilan hash qilinadi
- Session-based authentication
- Login/logout audit logging

### 2. Ma'lumotlar Bazasi Xavfsizligi
- Maxfiy ma'lumotlar AES-256 bilan shifrlangan
- Master key alohida faylda saqlanadi
- Database-level encryption

### 3. Kalit Boshqaruv Tizimi
- Kalitlar shifrlangan vault'da saqlanadi
- Avtomatik kalit generatsiya
- Kalit rotatsiya qo'llab-quvvatlash
- Har bir kalit uchun audit log

### 4. Audit Logging
- Barcha muhim harakatlar qayd etiladi
- Timestamp, user, action, details
- IP address tracking

## 📈 Tahlil Jarayoni

### 1. Ma'lumot Kiritish
- Matn kiritish
- Fayl yuklash (max 16MB)

### 2. Shifrlash va Tahlil
- Har bir algoritm bilan shifrlash
- Performance metrics yig'ish
- Security metrics hisoblash

### 3. Natijalarni Hisoblash
- T, E, K, I ko'rsatkichlarini hisoblash
- Umumiy S ballini hisoblash
- Eng yaxshi algoritmni aniqlash

### 4. Vizualizatsiya
- Interaktiv grafiklar yaratish
- Batafsil jadvallar ko'rsatish
- PDF hisobot generatsiya

## 🎓 Ilmiy Asos

### Tahlil Metodologiyasi
Loyiha quyidagi ilmiy tamoyillarga asoslangan:

1. **Multi-criteria Decision Analysis (MCDA)**
   - To'rt asosiy mezon (T, E, K, I)
   - Weighted scoring system
   - Normalization (0-1 range)

2. **Performance Benchmarking**
   - Vaqt o'lchash (millisekund aniqlik)
   - Resurs monitoring (CPU, RAM)
   - Statistical analysis

3. **Cryptographic Evaluation**
   - Shannon entropy calculation
   - Key size analysis
   - Security level assessment

4. **Quality Metrics**
   - Integrity verification
   - Consistency checking
   - Reliability testing

## 📊 Kutilgan Natijalar

### Algoritm Reytingi (Taxminiy)
1. **ChaCha20** - Eng tez va xavfsiz
2. **AES-256** - Eng keng qo'llaniladi
3. **Blowfish** - O'rta daraja
4. **DES** - Zaif, tavsiya etilmaydi

### Use Cases
- **AES:** Enterprise applications, file encryption
- **ChaCha20:** Mobile devices, real-time encryption
- **Blowfish:** Legacy systems, moderate security
- **DES:** Educational purposes only (deprecated)

## 🚀 Kelajakdagi Rivojlantirish

### Potensial Yangilanishlar
- [ ] Qo'shimcha algoritmlar (RSA, ECC)
- [ ] Parallel processing support
- [ ] Cloud deployment
- [ ] REST API
- [ ] Mobile application
- [ ] Multi-language support
- [ ] Advanced reporting
- [ ] Machine learning predictions

## 📚 Texnologiyalar Ro'yxati

### Backend
- Python 3.8+
- Flask 3.0.0
- SQLAlchemy 3.1.1
- cryptography 41.0.7
- pycryptodome 3.19.0
- psutil 5.9.6

### Frontend
- TailwindCSS 3.x
- Chart.js 4.4.0
- Alpine.js 3.x
- Font Awesome 6.4.2

### Tools
- WeasyPrint 60.1
- reportlab 4.0.7
- matplotlib 3.8.2

## 📝 Litsenziya
MIT License - Ochiq manba, bepul foydalanish

## 👥 Mualliflik
Intellektual Audit Modeli loyihasi - 2024

---

**Loyiha to'liq ishlab chiqildi va ishlatishga tayyor! 🎉**
