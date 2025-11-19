@echo off
REM Script per creare l'eseguibile Windows di VIES Checker

echo ========================================
echo VIES Checker - Build Script
echo ========================================
echo.

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato. Assicurati di averlo installato.
    pause
    exit /b 1
)

echo [1/4] Installazione dipendenze...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRORE: Impossibile installare le dipendenze.
    pause
    exit /b 1
)

echo.
echo [2/4] Pulizia build precedenti...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist vies_checker.spec del vies_checker.spec

echo.
echo [3/4] Creazione eseguibile con PyInstaller...
pyinstaller --onefile ^
    --name VIESChecker ^
    --icon=NONE ^
    --console ^
    --add-data "vies_api.py;." ^
    --add-data "database.py;." ^
    --add-data "excel_export.py;." ^
    vies_checker.py

if errorlevel 1 (
    echo ERRORE: Build fallita.
    pause
    exit /b 1
)

echo.
echo [4/4] Build completata!
echo.
echo L'eseguibile si trova in: dist\VIESChecker.exe
echo.
echo Puoi copiare VIESChecker.exe dove preferisci.
echo Il database vat_data.db verrà creato nella stessa cartella dell'eseguibile.
echo.
pause
