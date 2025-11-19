# Guida Interfaccia Grafica - VIES Checker

## Primo Avvio

1. **Doppio click** su `VIESCheckerGUI.exe`
2. Si aprirà la finestra principale del programma

## Schermata Principale

La finestra è divisa in 4 sezioni:

### 1. Verifica Partita IVA (in alto)
- Campo di input per inserire la partita IVA
- Pulsante "Verifica"
- Indicatore P.IVA Richiedente (se configurata)

### 2. Risultato Verifica (centro)
- Mostra il risultato dell'ultima verifica
- Colori: **Verde** = Valida, **Rosso** = Non Valida
- Tutti i dettagli della partita IVA verificata

### 3. Verifiche Recenti (in basso)
- Tabella con tutte le verifiche salvate
- **Doppio click** su una riga per vedere i dettagli
- Pulsanti per: Aggiorna Lista, Elimina, Esporta

### 4. Barra di Stato (in fondo)
- Mostra lo stato corrente dell'applicazione

## Come Verificare una Partita IVA

### Metodo 1: Veloce
1. Scrivi la P.IVA nel campo (es. `IT12345678901`)
2. Premi **INVIO**
3. Il risultato appare nella sezione "Risultato Verifica"

### Metodo 2: Con mouse
1. Scrivi la P.IVA nel campo
2. Clicca il pulsante **"Verifica"**
3. Attendi il risultato (qualche secondo)

## Configurare P.IVA Richiedente

### Perché configurarla?
La P.IVA richiedente è la **tua** partita IVA. Configurandola:
- Viene inviata automaticamente a ogni verifica
- Non devi reinserirla ogni volta
- Viene salvata permanentemente

### Come configurarla
1. Menu **Impostazioni** (in alto)
2. Clicca **"Configura P.IVA Richiedente"**
3. Inserisci la tua P.IVA (es. `IT00000000000`)
4. Clicca **"Salva"**

### Come rimuoverla
1. Menu **Impostazioni** > **"Configura P.IVA Richiedente"**
2. Cancella il campo (lascialo vuoto)
3. Clicca **"Salva"**

## Visualizzare lo Storico

### Vedere tutte le verifiche
- Guarda la tabella "Verifiche Recenti"
- Mostra le ultime 100 verifiche

### Vedere dettagli di una verifica
1. **Doppio click** sulla riga desiderata
2. I dettagli appaiono in "Risultato Verifica"

### Aggiornare la lista
- Clicca **"Aggiorna Lista"** in fondo alla tabella
- Utile se hai fatto verifiche da altre copie del programma

## Eliminare una Verifica

1. **Click singolo** sulla verifica da eliminare
2. Clicca **"Elimina Selezionata"**
3. Conferma cliccando **"Sì"**
4. La verifica viene rimossa dal database

## Esportare in Excel

### Esportare tutte le verifiche
1. Menu **File** > **"Esporta tutto in Excel"**
2. Scegli dove salvare il file
3. Scegli il nome del file
4. Clicca **"Salva"**

Il file Excel conterrà:
- Tutte le verifiche salvate
- Formattazione colorata
- Filtri automatici
- Colonne dimensionate

### Esportare solo le statistiche
1. Menu **File** > **"Esporta statistiche"**
2. Scegli dove salvare
3. Ottieni un riepilogo con:
   - Totale verifiche
   - Verifiche valide/non valide
   - Partite IVA uniche
   - Percentuale validità

## Menu dell'Applicazione

### Menu File
- **Esporta tutto in Excel** - Esporta tutte le verifiche
- **Esporta statistiche** - Crea riepilogo Excel
- **Esci** - Chiude il programma

### Menu Impostazioni
- **Configura P.IVA Richiedente** - Imposta la tua P.IVA

### Menu Aiuto
- **Come usare** - Breve guida inline
- **Informazioni** - Info sul programma

## Scorciatoie Tastiera

- **INVIO** (nel campo P.IVA) - Avvia verifica
- **DOPPIO CLICK** (su verifica) - Mostra dettagli
- **ALT+F4** - Chiude programma

## Interpretare i Risultati

### Partita IVA VALIDA ✓
- Testo verde
- "Valida: SI"
- Mostra Nome e Indirizzo dell'azienda
- La P.IVA è registrata nel database VIES

### Partita IVA NON VALIDA ✗
- Testo rosso
- "Valida: NO"
- Potrebbe mostrare un errore
- La P.IVA non è nel database VIES o è errata

## Possibili Errori

### "Errore VIES: ..."
- Il servizio VIES potrebbe essere temporaneamente non disponibile
- Riprova dopo qualche minuto
- Controlla la connessione Internet

### "Formato partita IVA non valido"
- Controlla di aver inserito il codice paese (es. IT, DE, FR)
- Esempio corretto: `IT12345678901`
- Esempio sbagliato: `12345678901` (manca IT)

### "Errore connessione al servizio VIES"
- Verifica la tua connessione Internet
- Il servizio VIES potrebbe essere in manutenzione
- Riprova più tardi

## File Creati dal Programma

Nella stessa cartella di `VIESCheckerGUI.exe` troverai:

- **vat_data.db** - Database con tutte le verifiche
- **vies_settings.json** - Impostazioni (P.IVA richiedente, ecc.)
- **vat_checks_*.xlsx** - File Excel esportati
- **vat_summary_*.xlsx** - Statistiche esportate

**IMPORTANTE**:
- NON cancellare `vat_data.db` se vuoi mantenere lo storico
- Puoi cancellare i file Excel se non servono più
- Puoi cancellare `vies_settings.json` per resettare le impostazioni

## Consigli per l'Uso

### Per verifiche singole
- Usa l'interfaccia grafica
- Veloce e intuitiva
- Ideale per controlli occasionali

### Per verifiche multiple
- Usa la versione CLI (`VIESChecker.exe`)
- Permette di inserire molte P.IVA in batch
- Più veloce per grandi quantità

### Backup dei dati
- Copia periodicamente `vat_data.db`
- Puoi ripristinarlo copiandolo nella stessa cartella
- Contiene tutte le tue verifiche

## Problemi Comuni

**Il programma non si avvia**
- Verifica di avere Python installato (solo per versione sorgente)
- Per l'eseguibile, non serve Python

**La verifica è lenta**
- Normale: il servizio VIES può richiedere 2-5 secondi
- Dipende dal carico del server VIES

**Non riesco a esportare in Excel**
- Controlla di avere i permessi di scrittura nella cartella
- Chiudi eventuali file Excel con lo stesso nome già aperti

**Le verifiche vecchie non compaiono**
- Clicca "Aggiorna Lista"
- Verifica che `vat_data.db` sia nella stessa cartella

## Supporto

Per problemi o domande:
- Leggi il file `README.md` completo
- Controlla la documentazione VIES: https://ec.europa.eu/taxation_customs/vies/
- Apri una issue su GitHub: https://github.com/alebaldo94/Vies-Cheker

---

**Buon utilizzo!** 🇪🇺
