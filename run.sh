#!/bin/bash

echo "============================================================"
echo "  Intellektual Audit Modeli - Ishga Tushirish"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual muhit topilmadi. Yaratilmoqda..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Virtual muhitni faollashtirish..."
source venv/bin/activate
echo ""

# Check if requirements are installed
echo "Kutubxonalarni tekshirish..."
if ! pip list | grep -q "Flask"; then
    echo "Kutubxonalar o'rnatilmoqda..."
    pip install -r requirements.txt
    echo ""
fi

# Initialize database if not exists
if [ ! -f "encryption_audit.db" ]; then
    echo "Ma'lumotlar bazasi yaratilmoqda..."
    python database/db_init.py
    echo ""
fi

# Run the application
echo "Ilova ishga tushirilmoqda..."
echo ""
python app.py
