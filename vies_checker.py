"""
VIES Checker - Programma per la verifica delle partite IVA europee
"""
import sys
import os

# Verifica versione Python
if sys.version_info < (3, 8):
    print("=" * 70)
    print("ERRORE: Versione Python non supportata")
    print("=" * 70)
    print(f"\nVersione Python rilevata: {sys.version}")
    print("\nQuesto programma richiede Python 3.8 o superiore.")
    print("Python 4 non esiste ancora - l'ultima versione è Python 3.x")
    print("\nPer favore:")
    print("1. Scarica Python 3.8 o superiore da: https://www.python.org/downloads/")
    print("2. Durante l'installazione, seleziona 'Add Python to PATH'")
    print("3. Riavvia il programma")
    print("\n" + "=" * 70)
    input("\nPremi INVIO per uscire...")
    sys.exit(1)

from vies_api import VIESChecker
from database import VATDatabase
from excel_export import ExcelExporter


class VIESCheckerApp:
    """Applicazione principale per la verifica delle partite IVA"""

    def __init__(self):
        """Inizializza l'applicazione"""
        self.checker = None
        self.db = VATDatabase()
        self.exporter = ExcelExporter()

    def initialize_checker(self):
        """Inizializza il checker VIES"""
        if self.checker is None:
            try:
                print("Connessione al servizio VIES in corso...")
                self.checker = VIESChecker()
                print("✓ Connesso al servizio VIES\n")
                return True
            except Exception as e:
                print(f"✗ Errore connessione VIES: {e}\n")
                return False
        return True

    def print_header(self):
        """Stampa l'header dell'applicazione"""
        print("=" * 70)
        print("VIES CHECKER - Verifica Partite IVA Europee".center(70))
        print("=" * 70)
        print()

    def print_menu(self):
        """Stampa il menu principale"""
        print("\n" + "-" * 70)
        print("MENU PRINCIPALE")
        print("-" * 70)
        print("1. Verifica singola partita IVA")
        print("2. Verifica multiple partite IVA")
        print("3. Visualizza tutte le verifiche")
        print("4. Cerca verifiche per partita IVA")
        print("5. Aggiorna verifica esistente")
        print("6. Esporta tutte le verifiche in Excel")
        print("7. Esporta riepilogo statistiche")
        print("8. Visualizza statistiche")
        print("9. Elimina verifica")
        print("0. Esci")
        print("-" * 70)

    def check_single_vat(self):
        """Verifica una singola partita IVA"""
        if not self.initialize_checker():
            return

        print("\n--- Verifica Singola Partita IVA ---")
        vat_number = input("Inserisci partita IVA (es. IT12345678901): ").strip()

        if not vat_number:
            print("✗ Partita IVA non valida")
            return

        print(f"\nVerifica in corso per {vat_number}...")
        result = self.checker.check_vat(vat_number)

        # Salva nel database
        self.db.save_check(result)

        # Mostra il risultato
        self.print_check_result(result)

    def check_multiple_vat(self):
        """Verifica multiple partite IVA"""
        if not self.initialize_checker():
            return

        print("\n--- Verifica Multiple Partite IVA ---")
        print("Inserisci le partite IVA una per riga.")
        print("Premi INVIO su una riga vuota per terminare.\n")

        vat_numbers = []
        while True:
            vat = input(f"Partita IVA #{len(vat_numbers) + 1} (o INVIO per terminare): ").strip()
            if not vat:
                break
            vat_numbers.append(vat)

        if not vat_numbers:
            print("✗ Nessuna partita IVA inserita")
            return

        print(f"\n\nVerifica di {len(vat_numbers)} partite IVA in corso...\n")

        valid_count = 0
        invalid_count = 0

        for i, vat_number in enumerate(vat_numbers, 1):
            print(f"[{i}/{len(vat_numbers)}] Verifica {vat_number}...", end=" ")
            result = self.checker.check_vat(vat_number)
            self.db.save_check(result)

            if result['valid']:
                print("✓ VALIDA")
                valid_count += 1
            else:
                print("✗ NON VALIDA")
                invalid_count += 1

        print(f"\n\nRiepilogo:")
        print(f"  Valide: {valid_count}")
        print(f"  Non valide: {invalid_count}")
        print(f"  Totale: {len(vat_numbers)}")

    def view_all_checks(self):
        """Visualizza tutte le verifiche"""
        print("\n--- Tutte le Verifiche ---")
        checks = self.db.get_all_checks()

        if not checks:
            print("Nessuna verifica trovata nel database.")
            return

        print(f"\nTotale verifiche: {len(checks)}\n")

        for check in checks:
            self.print_check_result(check)
            print("-" * 70)

    def search_by_vat(self):
        """Cerca verifiche per una specifica partita IVA"""
        print("\n--- Cerca Verifiche per P.IVA ---")
        vat_number = input("Inserisci partita IVA: ").strip().upper()

        if not vat_number:
            print("✗ Partita IVA non valida")
            return

        checks = self.db.get_checks_by_vat(vat_number)

        if not checks:
            print(f"\nNessuna verifica trovata per {vat_number}")
            return

        print(f"\n{len(checks)} verifica/e trovata/e per {vat_number}:\n")

        for check in checks:
            self.print_check_result(check)
            print("-" * 70)

    def update_check(self):
        """Aggiorna una verifica esistente"""
        if not self.initialize_checker():
            return

        print("\n--- Aggiorna Verifica ---")
        vat_number = input("Inserisci partita IVA da aggiornare: ").strip().upper()

        if not vat_number:
            print("✗ Partita IVA non valida")
            return

        # Mostra l'ultima verifica
        last_check = self.db.get_latest_check(vat_number)
        if last_check:
            print("\nUltima verifica trovata:")
            self.print_check_result(last_check)
        else:
            print(f"\nNessuna verifica precedente trovata per {vat_number}")

        confirm = input("\nConfermi l'aggiornamento? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operazione annullata")
            return

        print(f"\nVerifica in corso per {vat_number}...")
        result = self.checker.check_vat(vat_number)
        self.db.save_check(result)

        print("\n✓ Verifica aggiornata:")
        self.print_check_result(result)

    def export_all_to_excel(self):
        """Esporta tutte le verifiche in Excel"""
        print("\n--- Esporta in Excel ---")

        checks = self.db.get_all_checks()
        if not checks:
            print("Nessuna verifica da esportare.")
            return

        filename = input("Nome file (INVIO per nome automatico): ").strip()
        if not filename:
            filename = None

        try:
            saved_file = self.exporter.export_to_excel(checks, filename)
            print(f"\n✓ Dati esportati con successo in: {saved_file}")
            print(f"  Totale record esportati: {len(checks)}")
        except Exception as e:
            print(f"\n✗ Errore durante l'esportazione: {e}")

    def export_summary(self):
        """Esporta riepilogo statistiche in Excel"""
        print("\n--- Esporta Riepilogo ---")

        stats = self.db.get_stats()
        filename = input("Nome file (INVIO per nome automatico): ").strip()
        if not filename:
            filename = None

        try:
            saved_file = self.exporter.export_summary(stats, filename)
            print(f"\n✓ Riepilogo esportato con successo in: {saved_file}")
        except Exception as e:
            print(f"\n✗ Errore durante l'esportazione: {e}")

    def show_stats(self):
        """Visualizza statistiche"""
        print("\n--- Statistiche ---")
        stats = self.db.get_stats()

        print(f"\nTotale verifiche: {stats['total_checks']}")
        print(f"Verifiche valide: {stats['valid_checks']}")
        print(f"Verifiche non valide: {stats['invalid_checks']}")
        print(f"Partite IVA uniche: {stats['unique_vats']}")

        if stats['total_checks'] > 0:
            valid_percentage = (stats['valid_checks'] / stats['total_checks']) * 100
            print(f"\nPercentuale valide: {valid_percentage:.1f}%")

    def delete_check(self):
        """Elimina una verifica"""
        print("\n--- Elimina Verifica ---")

        try:
            check_id = int(input("Inserisci l'ID della verifica da eliminare: ").strip())
        except ValueError:
            print("✗ ID non valido")
            return

        confirm = input(f"Confermi l'eliminazione della verifica ID {check_id}? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operazione annullata")
            return

        if self.db.delete_check(check_id):
            print(f"✓ Verifica ID {check_id} eliminata con successo")
        else:
            print(f"✗ Verifica ID {check_id} non trovata")

    def print_check_result(self, result):
        """
        Stampa i risultati di una verifica in modo formattato

        Args:
            result (dict): Risultato della verifica
        """
        print(f"\nID: {result.get('id', 'N/A')}")
        print(f"Partita IVA: {result['vat_number']}")
        print(f"Codice Paese: {result['country_code']}")
        print(f"Valida: {'✓ SI' if result['valid'] else '✗ NO'}")

        if result['valid']:
            print(f"Nome/Ragione Sociale: {result['name']}")
            print(f"Indirizzo: {result['address']}")

        print(f"Data verifica: {result['request_date']}")

        if result['error']:
            print(f"Errore: {result['error']}")

    def run(self):
        """Avvia l'applicazione"""
        self.print_header()

        while True:
            self.print_menu()
            choice = input("\nScegli un'opzione: ").strip()

            if choice == '1':
                self.check_single_vat()
            elif choice == '2':
                self.check_multiple_vat()
            elif choice == '3':
                self.view_all_checks()
            elif choice == '4':
                self.search_by_vat()
            elif choice == '5':
                self.update_check()
            elif choice == '6':
                self.export_all_to_excel()
            elif choice == '7':
                self.export_summary()
            elif choice == '8':
                self.show_stats()
            elif choice == '9':
                self.delete_check()
            elif choice == '0':
                print("\nGrazie per aver utilizzato VIES Checker!")
                print("Arrivederci!\n")
                break
            else:
                print("\n✗ Opzione non valida. Riprova.")

            input("\nPremi INVIO per continuare...")


def main():
    """Funzione principale"""
    try:
        app = VIESCheckerApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nProgramma interrotto dall'utente.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nErrore critico: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
