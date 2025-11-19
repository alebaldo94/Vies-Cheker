#!/bin/bash
# Script per creare l'eseguibile di VIES Checker (Linux/Mac)

echo "========================================"
echo "VIES Checker - Build Script"
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
rm -rf build dist vies_checker.spec

echo ""
echo "[3/4] Creazione eseguibile con PyInstaller..."
pyinstaller --onefile \
    --name VIESChecker \
    --console \
    --add-data "vies_api.py:." \
    --add-data "database.py:." \
    --add-data "excel_export.py:." \
    vies_checker.py

if [ $? -ne 0 ]; then
    echo "ERRORE: Build fallita."
    exit 1
fi

echo ""
echo "[4/4] Build completata!"
echo ""
echo "L'eseguibile si trova in: dist/VIESChecker"
echo ""
echo "Puoi copiare VIESChecker dove preferisci."
echo "Il database vat_data.db verrà creato nella stessa cartella dell'eseguibile."
echo ""
