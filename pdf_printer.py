"""
Modulo per la stampa dei risultati in PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os


class PDFPrinter:
    """Classe per creare PDF stampabili delle verifiche"""

    def __init__(self):
        """Inizializza il generatore PDF"""
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()

    def create_custom_styles(self):
        """Crea stili personalizzati per il PDF"""
        # Titolo
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        # Label
        self.styles.add(ParagraphStyle(
            name='Label',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica-Bold'
        ))

        # Valore
        self.styles.add(ParagraphStyle(
            name='Value',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=10
        ))

        # Validità
        self.styles.add(ParagraphStyle(
            name='Valid',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.green,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='Invalid',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.red,
            fontName='Helvetica-Bold'
        ))

    def create_pdf_single_pages(self, checks, filename=None):
        """
        Crea un PDF con le verifiche (una per pagina)

        Args:
            checks (list): Lista di verifiche da stampare (già duplicate per copie)
            filename (str): Nome del file PDF (opzionale)

        Returns:
            str: Percorso del file creato
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"vat_print_{timestamp}.pdf"

        if not filename.endswith('.pdf'):
            filename += '.pdf'

        # Crea il documento
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Contenuto
        story = []

        # Per ogni verifica
        for check_idx, check in enumerate(checks):
            # Titolo
            story.append(Paragraph(
                "VERIFICA PARTITA IVA EUROPEA",
                self.styles['CustomTitle']
            ))
            story.append(Spacer(1, 0.5*cm))

            # Info sistema VIES
            story.append(Paragraph(
                "Sistema VIES - VAT Information Exchange System",
                self.styles['Normal']
            ))
            story.append(Paragraph(
                "Commissione Europea",
                self.styles['Normal']
            ))
            story.append(Spacer(1, 1.5*cm))

            # Dati verifica in tabella - ESTESA a tutta la larghezza A4
            data = []

            # Partita IVA
            data.append([
                Paragraph("<b>Partita IVA:</b>", self.styles['Label']),
                Paragraph(check['vat_number'], self.styles['Value'])
            ])

            # Codice Paese
            data.append([
                Paragraph("<b>Codice Paese:</b>", self.styles['Label']),
                Paragraph(check['country_code'], self.styles['Value'])
            ])

            # Validità
            valid_text = "✓ VALIDA" if check['valid'] else "✗ NON VALIDA"
            valid_style = 'Valid' if check['valid'] else 'Invalid'
            data.append([
                Paragraph("<b>Validità:</b>", self.styles['Label']),
                Paragraph(valid_text, self.styles[valid_style])
            ])

            if check['valid']:
                # Nome/Ragione Sociale
                if check['name']:
                    data.append([
                        Paragraph("<b>Nome/Ragione Sociale:</b>", self.styles['Label']),
                        Paragraph(check['name'], self.styles['Value'])
                    ])

                # Indirizzo
                if check['address']:
                    # Sostituisci newline con <br/>
                    address = check['address'].replace('\n', '<br/>')
                    data.append([
                        Paragraph("<b>Indirizzo:</b>", self.styles['Label']),
                        Paragraph(address, self.styles['Value'])
                    ])

            # P.IVA Richiedente
            if check.get('requester_vat'):
                data.append([
                    Paragraph("<b>P.IVA Richiedente:</b>", self.styles['Label']),
                    Paragraph(check['requester_vat'], self.styles['Value'])
                ])

            # Data verifica
            data.append([
                Paragraph("<b>Data Verifica:</b>", self.styles['Label']),
                Paragraph(check['request_date'], self.styles['Value'])
            ])

            # Errore (se presente)
            if check.get('error'):
                data.append([
                    Paragraph("<b>Errore:</b>", self.styles['Label']),
                    Paragraph(check['error'], self.styles['Value'])
                ])

            # Crea tabella ESTESA - usa tutta la larghezza disponibile dell'A4
            # A4 width = 21cm, margini 2cm sx + 2cm dx = 17cm disponibili
            table = Table(data, colWidths=[5*cm, 12*cm])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ]))

            story.append(table)
            story.append(Spacer(1, 2*cm))

            # Footer - SENZA NOTA LEGALE
            footer_text = f"Pagina {check_idx + 1} di {len(checks)} | Generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}"

            story.append(Paragraph(
                footer_text,
                self.styles['Normal']
            ))

            # Pagebreak (tranne per l'ultima pagina)
            if check_idx < len(checks) - 1:
                from reportlab.platypus import PageBreak
                story.append(PageBreak())

        # Genera il PDF
        doc.build(story)

        return filename
