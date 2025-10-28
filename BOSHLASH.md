# 🚀 Tezkor Boshlash

## 1-Qadam: .env Faylni Yaratish

```bash
python setup_env.py
```

Bu skript avtomatik ravishda xavfsiz MASTER_KEY va SECRET_KEY yaratadi.

## 2-Qadam: Dasturni Ishga Tushirish

```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

## 3-Qadam: Brauzerda Ochish

```
http://localhost:6001
```

**Standart foydalanuvchi:**
- Username: `admin`
- Password: `admin123`

## 4-Qadam: Xavfsiz Shifrlashni Sinab Ko'rish

1. Tizimga kiring
2. **Shifrlash** menyusiga o'ting
3. Algoritmni tanlang (AES tavsiya etiladi)
4. Faylni yuklang
5. **Shifrlash** tugmasini bosing
6. 2 ta faylni yuklab oling:
   - `filename.enc` - shifrlangan ma'lumot
   - `filename.key` - shifrlangan kalit

## 5-Qadam: Deshifrlashni Sinab Ko'rish

1. **Deshifrlash** menyusiga o'ting
2. Xuddi shu algoritmni tanlang
3. Ikkala faylni yuklang
4. **Deshifrlash** tugmasini bosing
5. Asl faylni yuklab oling

---

## ⚠️ Muhim Eslatmalar

- `.env` faylni **hech qachon** git'ga yuklashang
- `.env` fayldan **zaxira nusxa** oling
- **MASTER_KEY** ni o'zgartirmang (eski fayllar ishlamay qoladi)
- Shifrlash uchun **ikkala fayl** ham kerak

---

## 📖 To'liq Qo'llanma

Batafsil ma'lumot uchun `XAVFSIZ_SHIFRLASH.md` faylini o'qing.
