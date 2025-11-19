"""
Modulo per la gestione delle impostazioni dell'applicazione
"""
import json
import os


class Settings:
    """Classe per gestire le impostazioni dell'applicazione"""

    def __init__(self, settings_file='vies_settings.json'):
        """
        Inizializza le impostazioni

        Args:
            settings_file (str): Percorso del file impostazioni
        """
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self):
        """
        Carica le impostazioni dal file

        Returns:
            dict: Dizionario con le impostazioni
        """
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                # Se il file è corrotto, usa impostazioni di default
                return self.get_default_settings()
        else:
            return self.get_default_settings()

    def save_settings(self):
        """Salva le impostazioni nel file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore salvataggio impostazioni: {e}")
            return False

    def get_default_settings(self):
        """
        Restituisce le impostazioni di default

        Returns:
            dict: Impostazioni di default
        """
        return {
            'requester_vat': '',
            'window_width': 900,
            'window_height': 700,
            'theme': 'default'
        }

    def get(self, key, default=None):
        """
        Ottiene un valore dalle impostazioni

        Args:
            key (str): Chiave dell'impostazione
            default: Valore di default se la chiave non esiste

        Returns:
            Valore dell'impostazione
        """
        return self.settings.get(key, default)

    def set(self, key, value):
        """
        Imposta un valore nelle impostazioni

        Args:
            key (str): Chiave dell'impostazione
            value: Valore da impostare
        """
        self.settings[key] = value
        self.save_settings()

    def get_requester_vat(self):
        """
        Ottiene la partita IVA del richiedente salvata

        Returns:
            str: Partita IVA del richiedente
        """
        return self.settings.get('requester_vat', '')

    def set_requester_vat(self, vat_number):
        """
        Imposta la partita IVA del richiedente

        Args:
            vat_number (str): Partita IVA del richiedente
        """
        self.set('requester_vat', vat_number.strip().upper())

    def clear_requester_vat(self):
        """Cancella la partita IVA del richiedente"""
        self.set('requester_vat', '')
