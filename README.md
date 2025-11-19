# VIES Checker

Programma Windows per la verifica delle Partite IVA europee tramite il servizio VIES (VAT Information Exchange System) della Commissione Europea.

## Caratteristiche

✅ **Verifica Partite IVA** - Controllo in tempo reale tramite API VIES ufficiali
✅ **Memorizzazione Dati** - Salvataggio automatico di tutte le verifiche in database SQLite
✅ **Verifica Multipla** - Controllo di più partite IVA in una singola sessione
✅ **Esportazione Excel** - Genera report in formato Excel con formattazione
✅ **Aggiornamento** - Aggiorna le verifiche esistenti quando necessario
✅ **Statistiche** - Visualizza e esporta statistiche sulle verifiche effettuate
✅ **Interfaccia CLI** - Semplice interfaccia a linea di comando in italiano

## Requisiti

- Windows 7 o superiore (per l'eseguibile)
- Python 3.8+ (solo per sviluppo)
- Connessione Internet (per accedere alle API VIES)

## Installazione

### Opzione 1: Usa l'Eseguibile (Consigliato)

1. Scarica `VIESChecker.exe` dalla cartella `dist`
2. Copia l'eseguibile dove preferisci
3. Esegui `VIESChecker.exe`

**Nota**: Il database `vat_data.db` e i file Excel esportati verranno creati nella stessa cartella dell'eseguibile.

### Opzione 2: Esegui da Sorgente Python

1. Clona il repository:
   ```bash
   git clone https://github.com/alebaldo94/Vies-Cheker.git
   cd Vies-Cheker
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Esegui il programma:
   ```bash
   python vies_checker.py
   ```

## Creazione dell'Eseguibile

Per creare l'eseguibile Windows da sorgente:

### Su Windows:
```batch
build_exe.bat
```

### Su Linux/Mac:
```bash
chmod +x build_exe.sh
./build_exe.sh
```

L'eseguibile verrà creato nella cartella `dist/`.

## Utilizzo

Avvia il programma ed esplora il menu interattivo:

```
======================================================================
              VIES CHECKER - Verifica Partite IVA Europee
======================================================================

----------------------------------------------------------------------
MENU PRINCIPALE
----------------------------------------------------------------------
1. Verifica singola partita IVA
2. Verifica multiple partite IVA
3. Visualizza tutte le verifiche
4. Cerca verifiche per partita IVA
5. Aggiorna verifica esistente
6. Esporta tutte le verifiche in Excel
7. Esporta riepilogo statistiche
8. Visualizza statistiche
9. Elimina verifica
0. Esci
----------------------------------------------------------------------
```

### Esempi d'Uso

#### Verifica Singola Partita IVA
1. Seleziona opzione `1`
2. Inserisci la partita IVA (es. `IT12345678901`)
3. Il risultato verrà mostrato e salvato automaticamente

#### Verifica Multiple Partite IVA
1. Seleziona opzione `2`
2. Inserisci le partite IVA una per riga
3. Premi INVIO su una riga vuota per avviare le verifiche
4. Visualizza il riepilogo con conteggio valide/non valide

#### Esporta in Excel
1. Seleziona opzione `6` per esportare tutte le verifiche
2. Inserisci un nome file (opzionale)
3. Il file Excel verrà creato con formattazione colorata:
   - Verde = Partita IVA valida
   - Rosso = Partita IVA non valida

#### Aggiorna Verifica
1. Seleziona opzione `5`
2. Inserisci la partita IVA da aggiornare
3. Conferma l'aggiornamento
4. La nuova verifica verrà salvata mantenendo lo storico

## Formato Partita IVA

Le partite IVA devono essere inserite nel formato:
```
[CODICE_PAESE][NUMERO]
```

Esempi:
- `IT12345678901` (Italia)
- `DE123456789` (Germania)
- `FR12345678901` (Francia)
- `ES12345678X` (Spagna)

## Database

Il programma utilizza SQLite per memorizzare:
- Partita IVA completa
- Codice paese
- Validità (SI/NO)
- Nome/Ragione sociale
- Indirizzo
- Data e ora della verifica
- Eventuali errori

Il database viene creato automaticamente al primo avvio come `vat_data.db`.

## Export Excel

I file Excel esportati includono:

### Export Verifiche (`vat_checks_*.xlsx`)
- ID verifica
- Partita IVA
- Codice Paese
- Validità (con formattazione colorata)
- Nome/Ragione Sociale
- Indirizzo
- Data Verifica
- Eventuali Errori

### Export Riepilogo (`vat_summary_*.xlsx`)
- Totale verifiche
- Verifiche valide
- Verifiche non valide
- Partite IVA uniche
- Percentuale validità

## Struttura del Progetto

```
Vies-Cheker/
├── vies_checker.py      # Applicazione principale
├── vies_api.py          # Modulo per API VIES
├── database.py          # Modulo database SQLite
├── excel_export.py      # Modulo esportazione Excel
├── requirements.txt     # Dipendenze Python
├── build_exe.bat        # Script build Windows
├── build_exe.sh         # Script build Linux/Mac
├── .gitignore          # File da ignorare
└── README.md           # Questo file
```

## API VIES

Il programma utilizza il servizio ufficiale VIES della Commissione Europea:
- **URL WSDL**: https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl
- **Documentazione**: https://ec.europa.eu/taxation_customs/vies/

## Limitazioni

- Il servizio VIES potrebbe non essere sempre disponibile (manutenzione, sovraccarico)
- Alcune partite IVA potrebbero non essere presenti nel database VIES
- Il servizio è limitato alle partite IVA dell'Unione Europea
- Rate limiting: non effettuare troppe richieste consecutive

## Risoluzione Problemi

### Errore di connessione VIES
- Verifica la connessione Internet
- Controlla che il servizio VIES sia online
- Riprova dopo qualche minuto

### Partita IVA non valida (formato)
- Assicurati di includere il codice paese (2 lettere)
- Rimuovi spazi e caratteri speciali
- Usa lettere maiuscole

### Errore creazione eseguibile
- Verifica che Python 3.8+ sia installato
- Reinstalla le dipendenze: `pip install -r requirements.txt`
- Verifica che PyInstaller sia correttamente installato

## Dipendenze

- **requests** (2.31.0) - HTTP client
- **openpyxl** (3.1.2) - Lettura/scrittura file Excel
- **zeep** (4.2.1) - Client SOAP per API VIES
- **pyinstaller** (6.3.0) - Creazione eseguibili

## Licenza

Questo progetto è fornito "così com'è", senza garanzie di alcun tipo.

## Autore

Creato per semplificare la verifica delle partite IVA europee.

## Supporto

Per problemi o suggerimenti, apri una issue su GitHub.

---

**Nota**: Questo strumento è fornito a scopo informativo. La validazione VIES è indicativa e potrebbe non riflettere la situazione reale in tempo reale. Consulta sempre fonti ufficiali per verifiche critiche.
