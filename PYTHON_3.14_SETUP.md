# Guida Setup per Python 3.14

## ⚠️ IMPORTANTE: Python 4 NON Esiste!

Se vedi messaggi di errore che menzionano "Python 4", è un malinteso. **Python 4 non esiste ancora!** L'ultima versione stabile è Python 3.14.

## Setup con Python 3.14

Se hai Python 3.14 installato, segui questi passaggi:

### 1. Verifica la tua versione Python

```bash
python --version
```

Dovresti vedere qualcosa come: `Python 3.14.x` o `Python 3.13.x` o simile.

### 2. Installa le dipendenze

Il file `requirements.txt` è già configurato per Python 3.14. Esegui:

```bash
pip install -r requirements.txt
```

**NOTA**: Le vecchie versioni di PyInstaller (< 6.10.0) NON supportano Python 3.14. Il requirements.txt aggiornato usa PyInstaller >= 6.10.0 che è compatibile.

### 3. Verifica l'installazione

```bash
pip list
```

Dovresti vedere:
- `requests` (>= 2.28.0)
- `openpyxl` (>= 3.0.10)
- `zeep` (>= 4.1.0)
- `lxml` (>= 4.9.0)
- `pyinstaller` (>= 6.10.0)

### 4. Esegui il programma

```bash
python vies_checker.py
```

### 5. Crea l'eseguibile

Su Windows:
```bash
build_exe.bat
```

Su Linux/Mac:
```bash
./build_exe.sh
```

## Risoluzione Problemi

### Errore: "No matching distribution found for pyinstaller==6.3.0"

**Causa**: Stavi usando una versione vecchia del requirements.txt

**Soluzione**: Usa il requirements.txt aggiornato che specifica `pyinstaller>=6.10.0`

### Errore: "Requires-Python >=3.8,<3.14"

**Causa**: Alcune versioni di PyInstaller non supportano Python 3.14

**Soluzione**: Aggiorna PyInstaller:
```bash
pip install --upgrade pyinstaller
```

### Versioni Python Supportate

Questo programma funziona con:
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12
- ✅ Python 3.13
- ✅ Python 3.14
- ❌ Python 4 (non esiste!)

## Ancora Confuso?

Se vedi messaggi che parlano di "Python 4", ricorda:

1. **Python 4 non esiste** - è un errore di interpretazione
2. Il numero "4" che vedi potrebbe essere parte di un numero di versione di una libreria (es. zeep 4.2.1)
3. I messaggi tipo "Requires-Python >=3.8,<3.14" significano "richiede Python 3.8 o superiore, ma INFERIORE alla 3.14"

Se pip ti mostra molte versioni "ignorate", è normale - sta cercando versioni compatibili con la tua versione Python.

## Supporto

Per ulteriori problemi, apri una issue su GitHub con:
- Output di `python --version`
- Output di `pip list`
- Il messaggio di errore completo
