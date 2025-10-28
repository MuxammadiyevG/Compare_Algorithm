# 📁 Vaqtinchalik Fayllar Saqlash Tizimi

## 🔄 Yangi Yondashuv

Oldingi versiyada fayllar xotirada (session) saqlanardi. Endi **vaqtinchalik papkada** saqlanadi va yuklab olingandan keyin **avtomatik o'chiriladi**.

## 🎯 Asosiy G'oya

```
1. Foydalanuvchi faylni shifrlaydi
   ↓
2. Shifrlangan fayl va kalit temp_encrypted/ papkada saqlanadi
   ↓
3. Foydalanuvchi ikkala faylni yuklab oladi
   ↓
4. Ikkala fayl yuklab olingandan keyin papka o'chiriladi ✓
```

## 📂 Papka Strukturasi

```
temp_encrypted/
├── user_1/                    # Foydalanuvchi ID
│   ├── uuid-session-1/        # Shifrlash sessiyasi
│   │   ├── document.pdf.enc   # Shifrlangan fayl
│   │   └── document.pdf.key   # Shifrlangan kalit
│   └── uuid-session-2/
│       ├── photo.jpg.enc
│       └── photo.jpg.key
├── user_2/
│   └── uuid-session-3/
│       ├── file.txt.enc
│       └── file.txt.key
└── ...
```

## ⚙️ Qanday Ishlaydi?

### Shifrlash Jarayoni

```python
1. Fayl yuklash
2. Shifrlash (xotirada)
3. UUID sessiya yaratish
4. temp_encrypted/{user_id}/{session_id}/ papka yaratish
5. .enc va .key fayllarni papkaga saqlash
6. Session'da faqat session_id saqlash
```

### Yuklab Olish Jarayoni

```python
# .enc faylni yuklab olish
1. Session'dan session_id olish
2. Faylni topish va yuborish
3. enc_downloaded = True belgilash
4. Agar key_downloaded ham true bo'lsa → papkani o'chirish

# .key faylni yuklab olish
1. Session'dan session_id olish
2. Faylni topish va yuborish
3. key_downloaded = True belgilash
4. Agar enc_downloaded ham true bo'lsa → papkani o'chirish
```

### Deshifrlash Jarayoni

```python
1. Ikkala faylni yuklash
2. Deshifrlash (xotirada)
3. UUID sessiya yaratish
4. temp_encrypted/{user_id}/{session_id}/ papka yaratish
5. Deshifrlangan faylni saqlash
6. Foydalanuvchi yuklab oladi
7. Yuklab olingandan keyin papka o'chiriladi
```

## 🧹 Avtomatik Tozalash

### 1 Soatdan Eski Fayllar

Server ishga tushganda va har safar restart qilinganda:

```python
def cleanup_old_temp_files():
    """1 soatdan eski fayllarni o'chirish"""
    for user_folder in temp_encrypted:
        for session_folder in user_folder:
            if folder_age > 1_hour:
                delete(session_folder)
```

### Yuklab Olingandan Keyin

Ikkala fayl (.enc va .key) yuklab olingandan keyin:

```python
if enc_downloaded and key_downloaded:
    shutil.rmtree(session_folder)
```

## 🔒 Xavfsizlik

### ✅ Afzalliklar

1. **Foydalanuvchi Ajratish**
   - Har bir foydalanuvchi o'z papkasida
   - Boshqa foydalanuvchilar ko'ra olmaydi

2. **UUID Session**
   - Taxmin qilib bo'lmaydigan session ID
   - Xavfsiz fayl nomlari

3. **Avtomatik O'chirish**
   - Yuklab olingandan keyin darhol o'chiriladi
   - 1 soatdan eski fayllar tozalanadi

4. **Disk Saqlash**
   - Session hajmi cheklanmagan (session'da 4KB limit bor)
   - Katta fayllar bilan ishlash mumkin

### ⚠️ Xavfsizlik Choralari

1. **Login Talab**
   - Faqat tizimga kirgan foydalanuvchilar
   - User ID tekshiriladi

2. **Session Tekshiruvi**
   - Faqat o'z session'idagi fayllarni yuklab olish mumkin
   - Boshqa foydalanuvchi fayllariga kirish yo'q

3. **Vaqtinchalik Saqlash**
   - Fayllar faqat qisqa vaqt saqlanadi
   - Avtomatik tozalash

## 📊 Oldingi vs Yangi Yondashuv

| Xususiyat | Oldingi (Session) | Yangi (Temp Folder) |
|-----------|-------------------|---------------------|
| Saqlash joyi | Session (4KB limit) | Disk (cheksiz) |
| Katta fayllar | ❌ Muammo | ✅ Ishlaydi |
| O'chirish | Session tugashi | Yuklab olish + 1 soat |
| Xavfsizlik | ✅ Yaxshi | ✅ Yaxshi |
| Tezlik | ✅ Tez | ✅ Tez |
| Xotira | ❌ Ko'p ishlatadi | ✅ Kam ishlatadi |

## 🚀 Foydalanish

### Shifrlash

```bash
1. /secure-encrypt sahifasiga o'ting
2. Algoritmni tanlang
3. Faylni yuklang
4. "Shifrlash" tugmasini bosing
5. Ikkala faylni yuklab oling:
   - "Shifrlangan Fayl" tugmasi
   - "Shifrlangan Kalit" tugmasi
6. Fayllar yuklab olingandan keyin avtomatik o'chiriladi
```

### Deshifrlash

```bash
1. /secure-decrypt sahifasiga o'ting
2. Algoritmni tanlang
3. Ikkala faylni yuklang (.enc va .key)
4. "Deshifrlash" tugmasini bosing
5. "Asl Faylni Yuklab Olish" tugmasini bosing
6. Fayl yuklab olingandan keyin avtomatik o'chiriladi
```

## 🛠️ Texnik Tafsilotlar

### Konfiguratsiya

```python
# config.py
TEMP_ENCRYPTED_FOLDER = 'temp_encrypted/'
```

### Session Ma'lumotlari

```python
# Shifrlash
session['encryption_session_id'] = uuid
session['original_filename'] = filename
session['encryption_algorithm'] = algorithm
session['enc_downloaded'] = True/False
session['key_downloaded'] = True/False

# Deshifrlash
session['decryption_session_id'] = uuid
session['decrypted_filename'] = filename
```

### Fayl Yo'llari

```python
# Shifrlash
enc_path = temp_encrypted/{user_id}/{session_id}/{filename}.enc
key_path = temp_encrypted/{user_id}/{session_id}/{filename}.key

# Deshifrlash
decrypted_path = temp_encrypted/{user_id}/{session_id}/{filename}
```

## 🧪 Test Ssenariylari

### ✅ Test 1: Oddiy Shifrlash
```
1. Fayl yuklash
2. Shifrlash
3. .enc yuklab olish
4. .key yuklab olish
5. Papka o'chirilganini tekshirish ✓
```

### ✅ Test 2: Faqat Bitta Fayl Yuklab Olish
```
1. Fayl yuklash
2. Shifrlash
3. Faqat .enc yuklab olish
4. Papka hali mavjud ✓
5. 1 soatdan keyin avtomatik o'chiriladi ✓
```

### ✅ Test 3: Deshifrlash
```
1. .enc va .key yuklash
2. Deshifrlash
3. Asl faylni yuklab olish
4. Papka o'chirilganini tekshirish ✓
```

### ✅ Test 4: Bir Nechta Foydalanuvchi
```
1. User1 shifrlaydi
2. User2 shifrlaydi
3. Har biri o'z papkasida ✓
4. Bir-birining fayllarini ko'ra olmaydi ✓
```

## 📝 Kod Misollari

### Shifrlash

```python
@app.route('/secure-encrypt', methods=['POST'])
def secure_encrypt():
    # 1. Faylni shifrlash (xotirada)
    encrypted_data, encrypted_key = encrypt(file)
    
    # 2. Session yaratish
    session_id = str(uuid.uuid4())
    
    # 3. Papka yaratish
    folder = f"temp_encrypted/{user_id}/{session_id}/"
    os.makedirs(folder)
    
    # 4. Fayllarni saqlash
    save(folder + "file.enc", encrypted_data)
    save(folder + "file.key", encrypted_key)
    
    # 5. Session'da saqlash
    session['encryption_session_id'] = session_id
```

### Yuklab Olish

```python
@app.route('/download-encrypted-data')
def download_encrypted_data():
    # 1. Session'dan olish
    session_id = session['encryption_session_id']
    
    # 2. Faylni topish
    path = f"temp_encrypted/{user_id}/{session_id}/file.enc"
    
    # 3. Yuborish
    response = send_file(path)
    
    # 4. Belgilash
    session['enc_downloaded'] = True
    
    # 5. Agar ikkisi ham yuklab olingan bo'lsa
    if session['key_downloaded']:
        shutil.rmtree(folder)  # O'chirish
    
    return response
```

## 🔮 Kelajak Yaxshilanishlar

- [ ] Batch download (zip fayl)
- [ ] Progress bar
- [ ] Fayl hajmi statistikasi
- [ ] Tozalash jadvalini sozlash
- [ ] Email orqali fayl yuborish
- [ ] QR code orqali ulashish

## 📞 Yordam

### Muammolar

**Fayl topilmadi:**
- Session tugagan bo'lishi mumkin
- 1 soatdan oshgan bo'lishi mumkin
- Allaqachon yuklab olingan

**Papka o'chirilmadi:**
- Faqat bitta fayl yuklab olingan
- 1 soat kutish kerak

---

**Versiya:** v2.2.0  
**Yondashuv:** Vaqtinchalik Papka Saqlash  
**Avtomatik O'chirish:** ✅ Yoqilgan
