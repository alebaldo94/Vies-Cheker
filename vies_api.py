"""
Modulo per l'interazione con le API VIES (VAT Information Exchange System)
"""
import re
from datetime import datetime
from zeep import Client
from zeep.exceptions import Fault


class VIESChecker:
    """Classe per verificare partite IVA tramite il servizio VIES"""

    WSDL_URL = 'https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'

    def __init__(self):
        """Inizializza il client SOAP"""
        try:
            self.client = Client(self.WSDL_URL)
        except Exception as e:
            raise Exception(f"Errore inizializzazione client VIES: {str(e)}")

    @staticmethod
    def parse_vat_number(vat_number):
        """
        Estrae il codice paese e il numero dalla partita IVA

        Args:
            vat_number (str): Partita IVA completa (es. IT12345678901)

        Returns:
            tuple: (country_code, vat_number)
        """
        vat_number = vat_number.strip().upper().replace(' ', '')

        # Estrae le prime 2 lettere come codice paese
        match = re.match(r'^([A-Z]{2})(.+)$', vat_number)
        if not match:
            raise ValueError(f"Formato partita IVA non valido: {vat_number}")

        country_code = match.group(1)
        number = match.group(2)

        return country_code, number

    def check_vat(self, vat_number):
        """
        Verifica una partita IVA tramite VIES

        Args:
            vat_number (str): Partita IVA da verificare

        Returns:
            dict: Dizionario con i risultati della verifica
        """
        try:
            country_code, number = self.parse_vat_number(vat_number)

            # Chiamata al servizio VIES
            result = self.client.service.checkVat(
                countryCode=country_code,
                vatNumber=number
            )

            return {
                'vat_number': f"{country_code}{number}",
                'country_code': country_code,
                'valid': result.valid,
                'name': result.name or '',
                'address': result.address or '',
                'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': None
            }

        except Fault as e:
            # Errore SOAP
            return {
                'vat_number': vat_number,
                'country_code': country_code if 'country_code' in locals() else '',
                'valid': False,
                'name': '',
                'address': '',
                'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': f"Errore VIES: {str(e)}"
            }

        except ValueError as e:
            # Formato non valido
            return {
                'vat_number': vat_number,
                'country_code': '',
                'valid': False,
                'name': '',
                'address': '',
                'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': str(e)
            }

        except Exception as e:
            # Altri errori
            return {
                'vat_number': vat_number,
                'country_code': '',
                'valid': False,
                'name': '',
                'address': '',
                'request_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'error': f"Errore generico: {str(e)}"
            }
