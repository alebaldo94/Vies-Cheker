# Guida Rapida - VIES Checker

## Installazione Rapida (Windows)

1. **Scarica** `VIESChecker.exe`
2. **Posizionalo** in una cartella a tua scelta
3. **Doppio click** su `VIESChecker.exe`

Fatto! Il programma è pronto all'uso.

## Primo Utilizzo

Quando avvii il programma vedrai il menu principale:

```
1. Verifica singola partita IVA
2. Verifica multiple partite IVA
...
```

### Verifica Veloce di una Partita IVA

1. Premi `1` e INVIO
2. Inserisci la partita IVA (es. `IT12345678901`)
3. Premi INVIO
4. Visualizza il risultato

### Verifica di Più Partite IVA

1. Premi `2` e INVIO
2. Inserisci le partite IVA, una per riga:
   ```
   IT12345678901
   DE123456789
   FR12345678901
   ```
3. Premi INVIO su una riga vuota
4. Attendi il completamento
5. Visualizza il riepilogo

### Esporta i Risultati in Excel

1. Premi `6` e INVIO
2. (Opzionale) Inserisci un nome file, oppure premi INVIO
3. Il file Excel verrà creato nella stessa cartella del programma

## Formato Partite IVA

**IMPORTANTE**: Le partite IVA devono iniziare con il codice paese (2 lettere)

✅ Corretto:
- `IT12345678901`
- `DE123456789`
- `FR12345678901`

❌ Sbagliato:
- `12345678901` (manca IT)
- `123456789` (manca DE)

## Partite IVA di Test

Puoi usare queste partite IVA per testare il programma:

### Valide (esempio)
- Italia: `IT00743110157` (Google Italy)
- Germania: `DE811569869` (BMW AG)
- Francia: `FR40303265045` (Apple France)

### Non Valide (esempio)
- `IT00000000000` (numero falso)
- `DE000000000` (numero falso)

**Nota**: I numeri potrebbero cambiare. Usa il database VIES ufficiale per verifiche reali.

## File Creati dal Programma

Il programma crea questi file nella sua cartella:

- `vat_data.db` - Database con tutte le verifiche
- `vat_checks_*.xlsx` - Export Excel delle verifiche
- `vat_summary_*.xlsx` - Export statistiche

## Domande Frequenti

**D: Il programma dice "Errore connessione VIES"**
R: Verifica la tua connessione Internet e riprova. Il servizio VIES potrebbe essere temporaneamente non disponibile.

**D: La partita IVA risulta non valida ma è corretta**
R: Alcune partite IVA potrebbero non essere nel database VIES o richiedere tempo per l'aggiornamento. Consulta sempre fonti ufficiali.

**D: Posso verificare partite IVA non europee?**
R: No, il servizio VIES copre solo l'Unione Europea.

**D: Dove trovo i file Excel esportati?**
R: Nella stessa cartella dove si trova `VIESChecker.exe`.

**D: Posso cancellare il database?**
R: Sì, puoi cancellare `vat_data.db` per ricominciare da zero. Verrà ricreato automaticamente.

## Supporto

Per problemi o domande:
- Leggi il file `README.md` completo
- Controlla la documentazione VIES: https://ec.europa.eu/taxation_customs/vies/
- Apri una issue su GitHub

---

**Buona verifica!** 🇪🇺
