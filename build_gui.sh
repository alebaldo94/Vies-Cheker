#!/bin/bash
# Script per creare l'eseguibile GUI di VIES Checker (Linux/Mac)

echo "========================================"
echo "VIES Checker GUI - Build Script"
echo "========================================"
echo ""

# Verifica che Python sia installato
if ! command -v python3 &> /dev/null; then
    echo "ERRORE: Python 3 non trovato. Assicurati di averlo installato."
    exit 1
fi

echo "[1/4] Installazione dipendenze..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRORE: Impossibile installare le dipendenze."
    exit 1
fi

echo ""
echo "[2/4] Pulizia build precedenti..."
rm -rf build dist vies_checker_gui.spec

echo ""
echo "[3/4] Creazione eseguibile GUI con PyInstaller..."
pyinstaller --onefile \
    --name VIESCheckerGUI \
    --windowed \
    --add-data "vies_api.py:." \
    --add-data "database.py:." \
    --add-data "excel_export.py:." \
    --add-data "settings.py:." \
    --add-data "pdf_printer.py:." \
    vies_checker_gui.py

if [ $? -ne 0 ]; then
    echo "ERRORE: Build fallita."
    exit 1
fi

echo ""
echo "[4/4] Build completata!"
echo ""
echo "L'eseguibile GUI si trova in: dist/VIESCheckerGUI"
echo ""
echo "Puoi copiare VIESCheckerGUI dove preferisci."
echo "Il database vat_data.db e le impostazioni vies_settings.json"
echo "verranno creati nella stessa cartella dell'eseguibile."
echo ""
echo "NOTA: Questo eseguibile ha interfaccia grafica."
echo "      Per la versione CLI, usa build_exe.sh"
echo ""
