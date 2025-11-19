"""
Modulo per la gestione del database SQLite
"""
import sqlite3
import os
from datetime import datetime


class VATDatabase:
    """Classe per gestire il database delle partite IVA"""

    def __init__(self, db_path='vat_data.db'):
        """
        Inizializza il database

        Args:
            db_path (str): Percorso del file database
        """
        self.db_path = db_path
        self.conn = None
        self.create_table()

    def connect(self):
        """Crea una connessione al database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        """Chiude la connessione al database"""
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Crea la tabella se non esiste"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vat_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vat_number TEXT NOT NULL,
                country_code TEXT,
                valid INTEGER,
                name TEXT,
                address TEXT,
                requester_vat TEXT,
                request_date TEXT,
                error TEXT,
                UNIQUE(vat_number, request_date)
            )
        ''')

        # Aggiunge la colonna requester_vat se la tabella esiste già senza questa colonna
        try:
            cursor.execute('ALTER TABLE vat_checks ADD COLUMN requester_vat TEXT')
            conn.commit()
        except sqlite3.OperationalError:
            # La colonna esiste già
            pass

        # Crea un indice per velocizzare le ricerche
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_vat_number
            ON vat_checks(vat_number)
        ''')

        conn.commit()
        self.close()

    def save_check(self, check_result):
        """
        Salva il risultato di una verifica nel database

        Args:
            check_result (dict): Risultato della verifica VIES

        Returns:
            int: ID del record inserito
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO vat_checks
            (vat_number, country_code, valid, name, address, requester_vat, request_date, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            check_result['vat_number'],
            check_result['country_code'],
            1 if check_result['valid'] else 0,
            check_result['name'],
            check_result['address'],
            check_result.get('requester_vat', ''),
            check_result['request_date'],
            check_result['error']
        ))

        conn.commit()
        last_id = cursor.lastrowid
        self.close()

        return last_id

    def get_all_checks(self):
        """
        Recupera tutte le verifiche dal database

        Returns:
            list: Lista di dizionari con i risultati
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM vat_checks
            ORDER BY request_date DESC
        ''')

        rows = cursor.fetchall()
        self.close()

        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'vat_number': row['vat_number'],
                'country_code': row['country_code'],
                'valid': bool(row['valid']),
                'name': row['name'],
                'address': row['address'],
                'requester_vat': row.get('requester_vat', '') if isinstance(row, dict) else (row['requester_vat'] if 'requester_vat' in row.keys() else ''),
                'request_date': row['request_date'],
                'error': row['error']
            })

        return results

    def get_checks_by_vat(self, vat_number):
        """
        Recupera tutte le verifiche per una specifica partita IVA

        Args:
            vat_number (str): Partita IVA da cercare

        Returns:
            list: Lista di dizionari con i risultati
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM vat_checks
            WHERE vat_number = ?
            ORDER BY request_date DESC
        ''', (vat_number,))

        rows = cursor.fetchall()
        self.close()

        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'vat_number': row['vat_number'],
                'country_code': row['country_code'],
                'valid': bool(row['valid']),
                'name': row['name'],
                'address': row['address'],
                'requester_vat': row.get('requester_vat', '') if isinstance(row, dict) else (row['requester_vat'] if 'requester_vat' in row.keys() else ''),
                'request_date': row['request_date'],
                'error': row['error']
            })

        return results

    def get_latest_check(self, vat_number):
        """
        Recupera l'ultima verifica per una partita IVA

        Args:
            vat_number (str): Partita IVA da cercare

        Returns:
            dict or None: Risultato della verifica o None
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM vat_checks
            WHERE vat_number = ?
            ORDER BY request_date DESC
            LIMIT 1
        ''', (vat_number,))

        row = cursor.fetchone()
        self.close()

        if row:
            return {
                'id': row['id'],
                'vat_number': row['vat_number'],
                'country_code': row['country_code'],
                'valid': bool(row['valid']),
                'name': row['name'],
                'address': row['address'],
                'requester_vat': row['requester_vat'] if 'requester_vat' in row.keys() else '',
                'request_date': row['request_date'],
                'error': row['error']
            }

        return None

    def delete_check(self, check_id):
        """
        Elimina una verifica dal database

        Args:
            check_id (int): ID della verifica da eliminare

        Returns:
            bool: True se eliminata, False altrimenti
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM vat_checks WHERE id = ?', (check_id,))
        conn.commit()

        deleted = cursor.rowcount > 0
        self.close()

        return deleted

    def get_stats(self):
        """
        Recupera statistiche sulle verifiche

        Returns:
            dict: Statistiche
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Totale verifiche
        cursor.execute('SELECT COUNT(*) as total FROM vat_checks')
        total = cursor.fetchone()['total']

        # Verifiche valide
        cursor.execute('SELECT COUNT(*) as valid FROM vat_checks WHERE valid = 1')
        valid = cursor.fetchone()['valid']

        # Verifiche non valide
        cursor.execute('SELECT COUNT(*) as invalid FROM vat_checks WHERE valid = 0')
        invalid = cursor.fetchone()['invalid']

        # Partite IVA uniche
        cursor.execute('SELECT COUNT(DISTINCT vat_number) as unique_vats FROM vat_checks')
        unique_vats = cursor.fetchone()['unique_vats']

        self.close()

        return {
            'total_checks': total,
            'valid_checks': valid,
            'invalid_checks': invalid,
            'unique_vats': unique_vats
        }

    def update_check_by_vat(self, vat_number, check_result):
        """
        Aggiorna una verifica esistente per una specifica partita IVA
        Se non esiste, la crea

        Args:
            vat_number (str): Partita IVA da aggiornare
            check_result (dict): Risultato della verifica VIES

        Returns:
            bool: True se aggiornato, False se creato nuovo
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Cerca se esiste già un record per questa P.IVA
        cursor.execute('''
            SELECT id FROM vat_checks
            WHERE vat_number = ?
            ORDER BY request_date DESC
            LIMIT 1
        ''', (vat_number.strip().upper(),))

        existing = cursor.fetchone()

        if existing:
            # Aggiorna il record esistente
            cursor.execute('''
                UPDATE vat_checks
                SET country_code = ?,
                    valid = ?,
                    name = ?,
                    address = ?,
                    requester_vat = ?,
                    request_date = ?,
                    error = ?
                WHERE id = ?
            ''', (
                check_result['country_code'],
                1 if check_result['valid'] else 0,
                check_result['name'],
                check_result['address'],
                check_result.get('requester_vat', ''),
                check_result['request_date'],
                check_result['error'],
                existing['id']
            ))
            conn.commit()
            self.close()
            return True
        else:
            # Crea nuovo record
            self.close()
            self.save_check(check_result)
            return False

    def check_duplicate(self, vat_number, hours=24):
        """
        Verifica se una partita IVA è stata controllata recentemente

        Args:
            vat_number (str): Partita IVA da verificare
            hours (int): Numero di ore da considerare (default 24)

        Returns:
            dict or None: L'ultima verifica se trovata entro il periodo, None altrimenti
        """
        from datetime import datetime, timedelta

        conn = self.connect()
        cursor = conn.cursor()

        # Calcola il timestamp minimo
        min_date = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('''
            SELECT * FROM vat_checks
            WHERE vat_number = ? AND request_date >= ?
            ORDER BY request_date DESC
            LIMIT 1
        ''', (vat_number.strip().upper(), min_date))

        row = cursor.fetchone()
        self.close()

        if row:
            return {
                'id': row['id'],
                'vat_number': row['vat_number'],
                'country_code': row['country_code'],
                'valid': bool(row['valid']),
                'name': row['name'],
                'address': row['address'],
                'requester_vat': row['requester_vat'] if 'requester_vat' in row.keys() else '',
                'request_date': row['request_date'],
                'error': row['error']
            }

        return None
