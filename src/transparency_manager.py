import os
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from models import ListaTrasparenza, ModificaListaTrasparenza
from PyPDF2 import PdfReader

class TransparencyManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db')
        self.Session = sessionmaker(bind=self.engine)
        self.base_url = "https://www.aifa.gov.it"

    def download_latest_list(self):
        """Scarica l'ultima lista di trasparenza disponibile"""
        print("Tentativo di download della lista...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive'
        }
        try:
            url = f"{self.base_url}/liste-di-trasparenza"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                if 'Lista_farmaci_equivalenti_Principio_Attivo' in link['href']:
                    pdf_url = link['href']
                    if not pdf_url.startswith('http'):
                        pdf_url = f"{self.base_url}{pdf_url}"
                    
                    print(f"Trovato link PDF: {pdf_url}")
                    response = requests.get(pdf_url, headers=headers)
                    response.raise_for_status()
                    
                    filename = 'latest_list.pdf'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"PDF salvato come: {filename}")
                    return filename
            
            print("Nessun link PDF trovato nella pagina")
            return None
            
        except Exception as e:
            print(f"Errore durante il download: {e}")
            return None

    def parse_pdf_and_save(self, pdf_path):
        """Parse il PDF e salva i dati nel database"""
        session = self.Session()
        records_added = 0
        
        try:
            reader = PdfReader(pdf_path)
            current_date = datetime.now().date()
            print(f"Analisi PDF: {pdf_path}")
            
            for page_num, page in enumerate(reader.pages, 1):
                print(f"Analisi pagina {page_num}...")
                text = page.extract_text()
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line or 'Principio attivo' in line:
                        continue
                        
                    try:
                        # Stampa la riga per debug
                        print(f"Analisi riga: {line[:100]}...")
                        fields = [f.strip() for f in line.split('\t')]
                        
                        # Se non c'è un tab, prova a dividere per spazi multipli
                        if len(fields) < 3:
                            fields = [f.strip() for f in line.split('   ') if f.strip()]
                        
                        if len(fields) >= 3:
                            # Cerca il prezzo nell'ultimo campo
                            prezzo_str = fields[-1].replace('€', '').replace(',', '.').strip()
                            try:
                                prezzo = float(prezzo_str)
                            except ValueError:
                                print(f"Errore conversione prezzo: {prezzo_str}")
                                continue
                            
                            farmaco = ListaTrasparenza(
                                principio_attivo=fields[0],
                                nome_commerciale=fields[1] if len(fields) > 1 else '',
                                produttore=fields[2] if len(fields) > 2 else '',
                                prezzo=prezzo,
                                data_aggiornamento=current_date
                            )
                            session.add(farmaco)
                            records_added += 1
                            
                            if records_added % 50 == 0:
                                print(f"Processati {records_added} record...")
                                session.commit()
                    
                    except Exception as e:
                        print(f"Errore parsing riga: {e}")
                        continue
            
            session.commit()
            print(f"Salvati {records_added} record nel database")
            return records_added > 0
            
        except Exception as e:
            print(f"Errore durante il parsing del PDF: {e}")
            session.rollback()
            return False
            
        finally:
            session.close()

    def get_recent_documents(self):
        """Recupera i 5 documenti correlati più recenti"""
        session = self.Session()
        try:
            query = text("""
                SELECT DISTINCT data_aggiornamento, 
                       COUNT(*) as totale_farmaci,
                       COUNT(CASE WHEN prezzo > 0 THEN 1 END) as farmaci_con_prezzo
                FROM liste_trasparenza
                GROUP BY data_aggiornamento
                ORDER BY data_aggiornamento DESC
                LIMIT 5
            """)
            result = session.execute(query)
            documents = [dict(r) for r in result]
            print(f"Trovati {len(documents)} documenti recenti")
            return documents
        finally:
            session.close()

    def get_changes(self):
        """Recupera le modifiche tra l'ultima lista e quella precedente"""
        session = self.Session()
        try:
            dates = session.execute(text("""
                SELECT DISTINCT data_aggiornamento 
                FROM liste_trasparenza 
                ORDER BY data_aggiornamento DESC 
                LIMIT 2
            """)).fetchall()
            
            if len(dates) < 2:
                return None
                
            latest_date = dates[0][0]
            previous_date = dates[1][0]
            
            changes = {
                'nuovi': [],
                'rimossi': [],
                'modifiche_prezzo': []
            }
            
            # Trova nuovi farmaci
            new_query = text("""
                SELECT l.* FROM liste_trasparenza l
                WHERE l.data_aggiornamento = :latest_date
                AND NOT EXISTS (
                    SELECT 1 FROM liste_trasparenza p
                    WHERE p.data_aggiornamento = :previous_date
                    AND p.principio_attivo = l.principio_attivo
                )
            """)
            
            changes['nuovi'] = [dict(r) for r in session.execute(
                new_query, 
                {'latest_date': latest_date, 'previous_date': previous_date}
            )]
            
            # Trova farmaci rimossi
            removed_query = text("""
                SELECT l.* FROM liste_trasparenza l
                WHERE l.data_aggiornamento = :previous_date
                AND NOT EXISTS (
                    SELECT 1 FROM liste_trasparenza p
                    WHERE p.data_aggiornamento = :latest_date
                    AND p.principio_attivo = l.principio_attivo
                )
            """)
            
            changes['rimossi'] = [dict(r) for r in session.execute(
                removed_query, 
                {'latest_date': latest_date, 'previous_date': previous_date}
            )]
            
            # Trova modifiche di prezzo
            price_changes_query = text("""
                SELECT 
                    new.*, 
                    old.prezzo as prezzo_precedente
                FROM liste_trasparenza new
                JOIN liste_trasparenza old ON new.principio_attivo = old.principio_attivo
                WHERE new.data_aggiornamento = :latest_date
                AND old.data_aggiornamento = :previous_date
                AND new.prezzo != old.prezzo
            """)
            
            changes['modifiche_prezzo'] = [dict(r) for r in session.execute(
                price_changes_query,
                {'latest_date': latest_date, 'previous_date': previous_date}
            )]
            
            return changes
            
        finally:
            session.close()

    def update(self):
        """Aggiorna la lista di trasparenza"""
        pdf_path = self.download_latest_list()
        if not pdf_path:
            return False
        
        success = self.parse_pdf_and_save(pdf_path)
        
        # Pulisci il file temporaneo
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            
        return success

if __name__ == "__main__":
    manager = TransparencyManager()
    if manager.update():
        print("Aggiornamento completato con successo")
        changes = manager.get_changes()
        if changes:
            print(f"Nuovi farmaci: {len(changes['nuovi'])}")
            print(f"Farmaci rimossi: {len(changes['rimossi'])}")
            print(f"Modifiche prezzo: {len(changes['modifiche_prezzo'])}")
    else:
        print("Errore durante l'aggiornamento")