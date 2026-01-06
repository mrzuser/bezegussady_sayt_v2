@echo off
echo ==========================================
echo   Bezeg Ussady - Site Hazirlaniyor
echo ==========================================
echo.

echo 1. Adim: Gerekli kutuphaneler yukleniyor...
pip install flask
if %errorlevel% neq 0 (
    echo [UYARI] Yukleme sirasinda hata oldu ama devam ediliyor...
)

echo.
echo 2. Adim: Uygulama baslatiliyor...
echo ------------------------------------------
echo Tarayiciniz birazdan otomatik acilacak.
echo Kapatmak icin bu siyah pencereyi kapatin.
echo ------------------------------------------
echo.

python app.py

echo.
echo Program kapandi.
pause
