"""
VIES Checker - Interfaccia Grafica
Programma per la verifica delle partite IVA europee
"""
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
from datetime import datetime

# Verifica versione Python
if sys.version_info < (3, 8):
    print("ERRORE: Questo programma richiede Python 3.8 o superiore")
    sys.exit(1)

from vies_api import VIESChecker
from database import VATDatabase
from excel_export import ExcelExporter
from settings import Settings


class VIESCheckerGUI:
    """Interfaccia grafica per VIES Checker"""

    def __init__(self, root):
        """Inizializza l'interfaccia grafica"""
        self.root = root
        self.root.title("VIES Checker - Verifica Partite IVA Europee")
        self.root.geometry("950x750")

        # Configura l'icona (se disponibile)
        try:
            # Prova a impostare un'icona
            pass
        except:
            pass

        # Inizializza i componenti
        self.checker = None
        self.db = VATDatabase()
        self.exporter = ExcelExporter()
        self.settings = Settings()

        # Variabili
        self.vat_input_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto")

        # Crea l'interfaccia
        self.create_menu()
        self.create_widgets()

        # Carica verifiche recenti
        self.refresh_history()

        # Centra la finestra
        self.center_window()

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_menu(self):
        """Crea il menu dell'applicazione"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Esporta tutto in Excel", command=self.export_all)
        file_menu.add_command(label="Esporta statistiche", command=self.export_stats)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)

        # Menu Impostazioni
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Impostazioni", menu=settings_menu)
        settings_menu.add_command(label="Configura P.IVA Richiedente", command=self.show_settings_dialog)

        # Menu Aiuto
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aiuto", menu=help_menu)
        help_menu.add_command(label="Come usare", command=self.show_help)
        help_menu.add_command(label="Informazioni", command=self.show_about)

    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configura il ridimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # --- SEZIONE INPUT ---
        input_frame = ttk.LabelFrame(main_frame, text="Verifica Partita IVA", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        # Etichetta e campo input
        ttk.Label(input_frame, text="Partita IVA:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))

        vat_entry = ttk.Entry(input_frame, textvariable=self.vat_input_var, font=('Arial', 12))
        vat_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        vat_entry.bind('<Return>', lambda e: self.verify_vat())

        # Pulsante verifica
        verify_btn = ttk.Button(input_frame, text="Verifica", command=self.verify_vat)
        verify_btn.grid(row=0, column=2)

        # Info P.IVA richiedente
        requester_vat = self.settings.get_requester_vat()
        if requester_vat:
            info_text = f"P.IVA Richiedente: {requester_vat}"
        else:
            info_text = "Nessuna P.IVA richiedente configurata"

        self.requester_label = ttk.Label(input_frame, text=info_text, font=('Arial', 9), foreground='gray')
        self.requester_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))

        # --- SEZIONE RISULTATO ---
        result_frame = ttk.LabelFrame(main_frame, text="Risultato Verifica", padding="10")
        result_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)

        # Area risultato con scroll
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=8,
            font=('Courier New', 10),
            wrap=tk.WORD
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configura i tag per la colorazione
        self.result_text.tag_config('valid', foreground='green', font=('Courier New', 10, 'bold'))
        self.result_text.tag_config('invalid', foreground='red', font=('Courier New', 10, 'bold'))
        self.result_text.tag_config('label', foreground='blue', font=('Courier New', 10, 'bold'))

        # --- SEZIONE STORICO ---
        history_frame = ttk.LabelFrame(main_frame, text="Verifiche Recenti", padding="10")
        history_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        # Treeview per lo storico
        columns = ('ID', 'P.IVA', 'Valida', 'Nome/Ragione Sociale', 'Data')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)

        # Configura colonne
        self.history_tree.heading('ID', text='ID')
        self.history_tree.heading('P.IVA', text='Partita IVA')
        self.history_tree.heading('Valida', text='Valida')
        self.history_tree.heading('Nome/Ragione Sociale', text='Nome/Ragione Sociale')
        self.history_tree.heading('Data', text='Data Verifica')

        self.history_tree.column('ID', width=50, anchor=tk.CENTER)
        self.history_tree.column('P.IVA', width=150)
        self.history_tree.column('Valida', width=80, anchor=tk.CENTER)
        self.history_tree.column('Nome/Ragione Sociale', width=300)
        self.history_tree.column('Data', width=150)

        # Scrollbar per treeview
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)

        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind doppio click per visualizzare dettagli
        self.history_tree.bind('<Double-1>', self.show_detail)

        # Pulsanti azioni
        button_frame = ttk.Frame(history_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))

        ttk.Button(button_frame, text="Aggiorna Lista", command=self.refresh_history).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Elimina Selezionata", command=self.delete_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Esporta in Excel", command=self.export_all).pack(side=tk.LEFT)

        # --- BARRA DI STATO ---
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(0, weight=1)

        status_label = ttk.Label(status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def verify_vat(self):
        """Verifica una partita IVA"""
        vat_number = self.vat_input_var.get().strip()

        if not vat_number:
            messagebox.showwarning("Attenzione", "Inserisci una partita IVA da verificare")
            return

        # Esegue la verifica in un thread separato per non bloccare l'interfaccia
        self.status_var.set(f"Verifica in corso per {vat_number}...")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Verifica in corso...\n")

        thread = threading.Thread(target=self._verify_vat_thread, args=(vat_number,))
        thread.daemon = True
        thread.start()

    def _verify_vat_thread(self, vat_number):
        """Thread per la verifica (non blocca l'interfaccia)"""
        try:
            # Inizializza il checker se necessario
            if self.checker is None:
                self.checker = VIESChecker()

            # Ottiene la P.IVA richiedente dalle impostazioni
            requester_vat = self.settings.get_requester_vat()

            # Verifica
            result = self.checker.check_vat(vat_number, requester_vat if requester_vat else None)

            # Salva nel database
            self.db.save_check(result)

            # Aggiorna l'interfaccia nel thread principale
            self.root.after(0, self._display_result, result)

        except Exception as e:
            error_msg = f"Errore durante la verifica: {str(e)}"
            self.root.after(0, self._display_error, error_msg)

    def _display_result(self, result):
        """Visualizza il risultato della verifica"""
        self.result_text.delete(1.0, tk.END)

        # Formatta il risultato
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        self.result_text.insert(tk.END, "RISULTATO VERIFICA\n", 'label')
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")

        self.result_text.insert(tk.END, f"Partita IVA: ", 'label')
        self.result_text.insert(tk.END, f"{result['vat_number']}\n")

        self.result_text.insert(tk.END, f"Codice Paese: ", 'label')
        self.result_text.insert(tk.END, f"{result['country_code']}\n")

        self.result_text.insert(tk.END, f"Valida: ", 'label')
        if result['valid']:
            self.result_text.insert(tk.END, "SI\n", 'valid')
        else:
            self.result_text.insert(tk.END, "NO\n", 'invalid')

        if result['valid']:
            self.result_text.insert(tk.END, f"\nNome/Ragione Sociale: ", 'label')
            self.result_text.insert(tk.END, f"{result['name']}\n")

            self.result_text.insert(tk.END, f"Indirizzo: ", 'label')
            self.result_text.insert(tk.END, f"{result['address']}\n")

        if result.get('requester_vat'):
            self.result_text.insert(tk.END, f"\nP.IVA Richiedente: ", 'label')
            self.result_text.insert(tk.END, f"{result['requester_vat']}\n")

        self.result_text.insert(tk.END, f"\nData Verifica: ", 'label')
        self.result_text.insert(tk.END, f"{result['request_date']}\n")

        if result['error']:
            self.result_text.insert(tk.END, f"\nErrore: ", 'label')
            self.result_text.insert(tk.END, f"{result['error']}\n", 'invalid')

        self.result_text.insert(tk.END, "\n" + "=" * 60 + "\n")

        # Aggiorna lo storico
        self.refresh_history()

        # Aggiorna la barra di stato
        if result['valid']:
            self.status_var.set(f"Verifica completata: {result['vat_number']} - VALIDA")
        else:
            self.status_var.set(f"Verifica completata: {result['vat_number']} - NON VALIDA")

    def _display_error(self, error_msg):
        """Visualizza un errore"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, error_msg, 'invalid')
        self.status_var.set("Errore durante la verifica")
        messagebox.showerror("Errore", error_msg)

    def refresh_history(self):
        """Aggiorna la lista delle verifiche recenti"""
        # Cancella elementi esistenti
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Carica le ultime 100 verifiche
        checks = self.db.get_all_checks()[:100]

        for check in checks:
            valid_text = "SI" if check['valid'] else "NO"
            tags = ('valid',) if check['valid'] else ('invalid',)

            self.history_tree.insert(
                '',
                tk.END,
                values=(
                    check['id'],
                    check['vat_number'],
                    valid_text,
                    check['name'][:50] if check['name'] else '',
                    check['request_date']
                ),
                tags=tags
            )

        # Configura i tag per i colori
        self.history_tree.tag_configure('valid', foreground='green')
        self.history_tree.tag_configure('invalid', foreground='red')

        self.status_var.set(f"Caricate {len(checks)} verifiche recenti")

    def show_detail(self, event):
        """Mostra i dettagli di una verifica selezionata"""
        selection = self.history_tree.selection()
        if not selection:
            return

        item = self.history_tree.item(selection[0])
        check_id = item['values'][0]

        # Cerca la verifica nel database
        checks = self.db.get_all_checks()
        check = next((c for c in checks if c['id'] == check_id), None)

        if check:
            self._display_result(check)

    def delete_selected(self):
        """Elimina la verifica selezionata"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona una verifica da eliminare")
            return

        item = self.history_tree.item(selection[0])
        check_id = item['values'][0]
        vat_number = item['values'][1]

        if messagebox.askyesno("Conferma", f"Eliminare la verifica per {vat_number}?"):
            if self.db.delete_check(check_id):
                messagebox.showinfo("Successo", "Verifica eliminata")
                self.refresh_history()
            else:
                messagebox.showerror("Errore", "Impossibile eliminare la verifica")

    def export_all(self):
        """Esporta tutte le verifiche in Excel"""
        checks = self.db.get_all_checks()

        if not checks:
            messagebox.showwarning("Attenzione", "Nessuna verifica da esportare")
            return

        # Chiedi il nome del file
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"vat_checks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        if filename:
            try:
                self.exporter.export_to_excel(checks, filename)
                messagebox.showinfo("Successo", f"Dati esportati in:\n{filename}")
                self.status_var.set(f"Esportati {len(checks)} record in {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'esportazione:\n{str(e)}")

    def export_stats(self):
        """Esporta statistiche in Excel"""
        stats = self.db.get_stats()

        # Chiedi il nome del file
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"vat_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        if filename:
            try:
                self.exporter.export_summary(stats, filename)
                messagebox.showinfo("Successo", f"Statistiche esportate in:\n{filename}")
                self.status_var.set(f"Statistiche esportate in {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'esportazione:\n{str(e)}")

    def show_settings_dialog(self):
        """Mostra il dialogo impostazioni per P.IVA richiedente"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Impostazioni - P.IVA Richiedente")
        dialog.geometry("450x200")
        dialog.resizable(False, False)

        # Centra il dialogo
        dialog.transient(self.root)
        dialog.grab_set()

        # Frame principale
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Descrizione
        desc = ttk.Label(
            frame,
            text="Configura la tua Partita IVA da usare come richiedente.\n"
                 "Questa verrà utilizzata automaticamente per tutte le verifiche.",
            wraplength=400
        )
        desc.pack(pady=(0, 20))

        # Input frame
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(input_frame, text="P.IVA Richiedente:").pack(side=tk.LEFT, padx=(0, 10))

        requester_var = tk.StringVar(value=self.settings.get_requester_vat())
        requester_entry = ttk.Entry(input_frame, textvariable=requester_var, width=30)
        requester_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Bottoni
        button_frame = ttk.Frame(frame)
        button_frame.pack()

        def save_and_close():
            vat = requester_var.get().strip().upper()
            if vat:
                # Verifica il formato
                try:
                    from vies_api import VIESChecker
                    VIESChecker.parse_vat_number(vat)
                    self.settings.set_requester_vat(vat)
                    messagebox.showinfo("Successo", f"P.IVA Richiedente impostata:\n{vat}")
                    self.update_requester_label()
                    dialog.destroy()
                except ValueError as e:
                    messagebox.showerror("Errore", f"Formato P.IVA non valido:\n{str(e)}")
            else:
                self.settings.clear_requester_vat()
                messagebox.showinfo("Info", "P.IVA Richiedente rimossa")
                self.update_requester_label()
                dialog.destroy()

        ttk.Button(button_frame, text="Salva", command=save_and_close).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annulla", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        requester_entry.focus()

    def update_requester_label(self):
        """Aggiorna l'etichetta della P.IVA richiedente"""
        requester_vat = self.settings.get_requester_vat()
        if requester_vat:
            info_text = f"P.IVA Richiedente: {requester_vat}"
        else:
            info_text = "Nessuna P.IVA richiedente configurata"

        self.requester_label.config(text=info_text)

    def show_help(self):
        """Mostra la guida"""
        help_text = """
COME USARE VIES CHECKER

1. VERIFICA PARTITA IVA
   - Inserisci la partita IVA nel formato: CODICE_PAESE + NUMERO
     Esempio: IT12345678901, DE123456789, FR12345678901
   - Clicca "Verifica" o premi INVIO
   - Il risultato apparirà nella sezione "Risultato Verifica"

2. CONFIGURA P.IVA RICHIEDENTE (Opzionale)
   - Menu "Impostazioni" > "Configura P.IVA Richiedente"
   - Inserisci la tua partita IVA
   - Questa verrà usata automaticamente per tutte le verifiche

3. STORICO VERIFICHE
   - Tutte le verifiche vengono salvate automaticamente
   - Doppio click su una verifica per visualizzare i dettagli
   - Usa "Elimina Selezionata" per rimuovere una verifica

4. ESPORTAZIONE
   - Menu "File" > "Esporta tutto in Excel"
   - Scegli dove salvare il file Excel
   - Il file conterrà tutte le verifiche con formattazione

Per assistenza: https://github.com/alebaldo94/Vies-Cheker
        """

        messagebox.showinfo("Guida - VIES Checker", help_text)

    def show_about(self):
        """Mostra informazioni sul programma"""
        about_text = """
VIES CHECKER
Versione 2.0

Programma per la verifica delle Partite IVA europee
tramite il servizio VIES della Commissione Europea.

Caratteristiche:
• Verifica in tempo reale tramite API VIES ufficiali
• Salvataggio automatico di tutte le verifiche
• Configurazione P.IVA richiedente
• Esportazione in Excel con formattazione
• Interfaccia grafica semplice e intuitiva

Repository: https://github.com/alebaldo94/Vies-Cheker

Questo software è fornito "così com'è", senza garanzie.
        """

        messagebox.showinfo("Informazioni - VIES Checker", about_text)


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = VIESCheckerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
