@echo off
echo ============================================================
echo   Intellektual Audit Modeli - Ishga Tushirish
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual muhit topilmadi. Yaratilmoqda...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Virtual muhitni faollashtirish...
call venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
echo Kutubxonalarni tekshirish...
pip list | findstr "Flask" >nul
if errorlevel 1 (
    echo Kutubxonalar o'rnatilmoqda...
    pip install -r requirements.txt
    echo.
)

REM Initialize database if not exists
if not exist "encryption_audit.db" (
    echo Ma'lumotlar bazasi yaratilmoqda...
    python database\db_init.py
    echo.
)

REM Run the application
echo Ilova ishga tushirilmoqda...
echo.
python app.py

pause
