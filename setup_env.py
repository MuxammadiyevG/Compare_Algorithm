"""
Setup script to generate .env file with secure MASTER_KEY
Run this script once before starting the application
"""

import os
import base64
import secrets

def generate_master_key():
    """Generate a secure 256-bit (32-byte) master key"""
    return base64.b64encode(os.urandom(32)).decode()

def generate_secret_key():
    """Generate a secure Flask secret key"""
    return secrets.token_hex(32)

def create_env_file():
    """Create .env file with generated keys"""
    
    print("=" * 60)
    print("Xavfsiz Shifrlash Tizimi - .env Fayl Yaratish")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input(".env fayl allaqachon mavjud. Qayta yaratilsinmi? (y/n): ")
        if response.lower() != 'y':
            print("Bekor qilindi.")
            return
    
    print("Xavfsiz kalitlar yaratilmoqda...")
    print()
    
    # Generate keys
    master_key = generate_master_key()
    secret_key = generate_secret_key()
    
    # Create .env content
    env_content = f"""# Master encryption key for key wrapping (256-bit AES key in base64)
# DO NOT CHANGE THIS KEY - it's used to encrypt/decrypt session keys
# DO NOT SHARE THIS KEY - keep it secret and secure
MASTER_KEY={master_key}

# Flask configuration
SECRET_KEY={secret_key}

# Database configuration (optional, defaults to SQLite)
# DATABASE_URL=sqlite:///encryption_audit.db
"""
    
    # Write to .env file
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("[OK] .env fayl muvaffaqiyatli yaratildi!")
    print()
    print("=" * 60)
    print("MUHIM XAVFSIZLIK OGOHLANTIRISHI:")
    print("=" * 60)
    print("1. .env faylni hech kimga ko'rsatmang")
    print("2. .env faylni git repository'ga yuklashdan saqlaning")
    print("3. MASTER_KEY ni o'zgartirmang (mavjud shifrlangan fayllar ishlamay qoladi)")
    print("4. .env fayldan zaxira nusxa oling va xavfsiz joyda saqlang")
    print()
    print("Endi dasturni ishga tushirishingiz mumkin:")
    print("  Windows: run.bat")
    print("  Linux/Mac: ./run.sh")
    print("=" * 60)

if __name__ == '__main__':
    try:
        create_env_file()
    except Exception as e:
        print(f"Xatolik: {str(e)}")
        input("Davom etish uchun Enter tugmasini bosing...")
