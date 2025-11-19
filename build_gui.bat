@echo off
REM Script per creare l'eseguibile GUI Windows di VIES Checker

echo ========================================
echo VIES Checker GUI - Build Script
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
if exist vies_checker_gui.spec del vies_checker_gui.spec

echo.
echo [3/4] Creazione eseguibile GUI con PyInstaller...
pyinstaller --onefile ^
    --name VIESCheckerGUI ^
    --windowed ^
    --icon=NONE ^
    --add-data "vies_api.py;." ^
    --add-data "database.py;." ^
    --add-data "excel_export.py;." ^
    --add-data "settings.py;." ^
    --add-data "pdf_printer.py;." ^
    vies_checker_gui.py

if errorlevel 1 (
    echo ERRORE: Build fallita.
    pause
    exit /b 1
)

echo.
echo [4/4] Build completata!
echo.
echo L'eseguibile GUI si trova in: dist\VIESCheckerGUI.exe
echo.
echo Puoi copiare VIESCheckerGUI.exe dove preferisci.
echo Il database vat_data.db e le impostazioni vies_settings.json
echo verranno creati nella stessa cartella dell'eseguibile.
echo.
echo NOTA: Questo eseguibile ha interfaccia grafica (non mostra console).
echo       Per la versione CLI, usa build_exe.bat
echo.
pause
