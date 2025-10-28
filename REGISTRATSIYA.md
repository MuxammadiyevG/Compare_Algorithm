# 👤 Foydalanuvchi Registratsiyasi

## 📋 Umumiy Ma'lumot

Tizimga yangi foydalanuvchi registratsiyasi funksiyasi qo'shildi. Endi har bir foydalanuvchi o'z shaxsiy akkountini yaratishi mumkin.

## ✨ Yangi Xususiyatlar

### 1. **Registratsiya Sahifasi**
- Chiroyli va zamonaviy interfeys
- To'liq validatsiya
- Parolni ko'rish/yashirish funksiyasi
- Xatolik xabarlari

### 2. **Validatsiya**
- ✅ Barcha maydonlar to'ldirilishi shart
- ✅ Email formati tekshiriladi
- ✅ Parol kamida 6 ta belgidan iborat bo'lishi kerak
- ✅ Parollar mos kelishi kerak
- ✅ Foydalanuvchi nomi noyob bo'lishi kerak
- ✅ Email noyob bo'lishi kerak

### 3. **Xavfsizlik**
- Parollar hash qilinib saqlanadi (Werkzeug)
- Audit log yoziladi
- Session boshqaruvi

## 🚀 Qanday Ishlatish?

### Yangi Foydalanuvchi Yaratish

1. **Login sahifasiga o'ting**
   ```
   http://localhost:6001/login
   ```

2. **"Ro'yxatdan o'ting" havolasini bosing**

3. **Ma'lumotlarni kiriting:**
   - Foydalanuvchi nomi (username)
   - Email manzil
   - Parol (kamida 6 ta belgi)
   - Parolni tasdiqlash

4. **"Ro'yxatdan O'tish" tugmasini bosing**

5. **Muvaffaqiyatli ro'yxatdan o'tganingizdan keyin login sahifasiga yo'naltirilasiz**

6. **Yangi akkount bilan tizimga kiring**

## 📝 Misol

```
Foydalanuvchi nomi: john_doe
Email: john@example.com
Parol: mypassword123
Parolni tasdiqlash: mypassword123
```

## 🔒 Xavfsizlik

### Parol Xavfsizligi
- Parollar hech qachon ochiq ko'rinishda saqlanmaydi
- Werkzeug'ning `generate_password_hash` funksiyasi ishlatiladi
- SHA-256 hash algoritmi

### Audit Log
Har bir registratsiya audit logga yoziladi:
```
[2024-01-15 10:30:45] USER: john_doe | ACTION: REGISTER | DETAILS: New user registered: john_doe
```

## ⚠️ Muhim Eslatmalar

1. **Parolni unutmang!**
   - Parolni tiklash funksiyasi hozircha yo'q
   - Parolni xavfsiz joyda saqlang

2. **Email noyob bo'lishi kerak**
   - Bir email faqat bir marta ishlatilishi mumkin

3. **Foydalanuvchi nomi o'zgartirilmaydi**
   - Ro'yxatdan o'tgandan keyin username o'zgartirib bo'lmaydi

## 🛠️ Texnik Tafsilotlar

### Backend Route
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Validation
    # Create user
    # Hash password
    # Save to database
    # Log audit
    # Redirect to login
```

### Database Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Parol Hash
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash parol
user.set_password(password)  # generate_password_hash(password)

# Tekshirish
user.check_password(password)  # check_password_hash(hash, password)
```

## 📊 Foydalanuvchi Statistikasi

Har bir foydalanuvchi o'z shaxsiy:
- ✅ Tahlil natijalari
- ✅ Shifrlangan ma'lumotlar
- ✅ Audit log yozuvlari
- ✅ Hisobotlar

## 🔮 Kelajak Rejalari

- [ ] Parolni tiklash (email orqali)
- [ ] Profil tahrirlash
- [ ] Avatar yuklash
- [ ] 2FA (Two-Factor Authentication)
- [ ] Social login (Google, GitHub)
- [ ] Foydalanuvchi rollari (admin, user)

## 🐛 Muammolarni Hal Qilish

### "Bu foydalanuvchi nomi band!"
**Yechim:** Boshqa username tanlang

### "Bu email allaqachon ro'yxatdan o'tgan!"
**Yechim:** Boshqa email kiriting yoki login qiling

### "Parollar mos kelmadi!"
**Yechim:** Ikkala maydonni ham bir xil parol kiriting

### "Parol kamida 6 ta belgidan iborat bo'lishi kerak!"
**Yechim:** Uzunroq parol kiriting

## 📸 Screenshot

```
┌─────────────────────────────────────────┐
│     🧠 Intellektual Audit               │
│     Dasturiy Ta'minot Xavfsizligi       │
├─────────────────────────────────────────┤
│                                         │
│  👤 Ro'yxatdan O'tish                   │
│                                         │
│  Foydalanuvchi Nomi:                    │
│  [________________]                     │
│                                         │
│  Email:                                 │
│  [________________]                     │
│                                         │
│  Parol:                                 │
│  [________________] 👁                  │
│                                         │
│  Parolni Tasdiqlash:                    │
│  [________________] 👁                  │
│                                         │
│  [  Ro'yxatdan O'tish  ]                │
│                                         │
│  Allaqachon akkountingiz bormi?         │
│  Kirish                                 │
│                                         │
└─────────────────────────────────────────┘
```

## 📞 Yordam

Muammolar yoki savollar uchun:
- Admin bilan bog'laning
- Audit log tekshiring: `/logs/audit.log`

---

**Eslatma:** Standart admin akkaunt hali ham mavjud:
- Username: `admin`
- Password: `admin123`
