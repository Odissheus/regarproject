from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ListaTrasparenza, ModificaListaTrasparenza
import json
from datetime import datetime, timedelta

class TransparencyListChatbot:
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db')
        self.Session = sessionmaker(bind=self.engine)

    def process_query(self, query):
        """Processa una query dell'utente e restituisce una risposta appropriata"""
        query = query.lower()
        session = self.Session()
        
        try:
            # Ricerca per principio attivo
            if "prezzo" in query or "costo" in query:
                for principio in session.query(ListaTrasparenza.principio_attivo).distinct():
                    if principio[0].lower() in query:
                        result = session.query(ListaTrasparenza)\
                            .filter(ListaTrasparenza.principio_attivo == principio[0])\
                            .order_by(ListaTrasparenza.data_aggiornamento.desc())\
                            .first()
                        return f"Il prezzo attuale per {result.principio_attivo} è {result.prezzo}€"

            # Ultime modifiche
            if "ultim" in query and ("modific" in query or "aggiornament" in query):
                modifiche = session.query(ModificaListaTrasparenza)\
                    .order_by(ModificaListaTrasparenza.data_modifica.desc())\
                    .limit(5).all()
                
                response = "Ecco le ultime modifiche:\n"
                for modifica in modifiche:
                    response += f"- {modifica.data_modifica}: {modifica.tipo_modifica} per {modifica.principio_attivo}\n"
                return response

            # Statistiche generali
            if "statistic" in query or "riepilog" in query:
                oggi = datetime.now().date()
                un_mese_fa = oggi - timedelta(days=30)
                
                stats = {
                    "totale_farmaci": session.query(ListaTrasparenza)\
                        .filter(ListaTrasparenza.data_aggiornamento == oggi)\
                        .count(),
                    "nuovi_ultimo_mese": session.query(ModificaListaTrasparenza)\
                        .filter(ModificaListaTrasparenza.tipo_modifica == 'nuovo')\
                        .filter(ModificaListaTrasparenza.data_modifica >= un_mese_fa)\
                        .count(),
                    "modifiche_prezzo_ultimo_mese": session.query(ModificaListaTrasparenza)\
                        .filter(ModificaListaTrasparenza.tipo_modifica == 'modifica_prezzo')\
                        .filter(ModificaListaTrasparenza.data_modifica >= un_mese_fa)\
                        .count()
                }
                
                return f"""Statistiche attuali:
                    - Totale farmaci in lista: {stats['totale_farmaci']}
                    - Nuovi farmaci ultimo mese: {stats['nuovi_ultimo_mese']}
                    - Modifiche prezzo ultimo mese: {stats['modifiche_prezzo_ultimo_mese']}"""

            # Confronto prezzi
            if "confronta" in query or "differenza" in query:
                for principio in session.query(ListaTrasparenza.principio_attivo).distinct():
                    if principio[0].lower() in query:
                        modifiche = session.query(ModificaListaTrasparenza)\
                            .filter(ModificaListaTrasparenza.principio_attivo == principio[0])\
                            .filter(ModificaListaTrasparenza.tipo_modifica == 'modifica_prezzo')\
                            .order_by(ModificaListaTrasparenza.data_modifica.desc())\
                            .limit(5).all()
                            
                        if modifiche:
                            response = f"Storico modifiche prezzo per {principio[0]}:\n"
                            for modifica in modifiche:
                                dettagli = json.loads(modifica.dettagli_modifica)
                                response += f"- {modifica.data_modifica}: da {dettagli['prezzo_precedente']}€ a {dettagli['nuovo_prezzo']}€\n"
                            return response
                        return f"Non ci sono state modifiche recenti di prezzo per {principio[0]}"

            # Risposta di default
            return """Posso aiutarti con:
                - Ricerca prezzo di un farmaco
                - Ultime modifiche alla lista
                - Statistiche generali
                - Confronto prezzi nel tempo
                Specificami cosa ti interessa."""

        finally:
            session.close()

def test_chatbot():
    chatbot = TransparencyListChatbot()
    
    # Test domande diverse
    test_queries = [
        "Qual è il prezzo del paracetamolo?",
        "Quali sono le ultime modifiche?",
        "Dammi le statistiche generali",
        "Confronta i prezzi dell'ibuprofene",
    ]
    
    for query in test_queries:
        print(f"\nDomanda: {query}")
        print(f"Risposta: {chatbot.process_query(query)}")

if __name__ == "__main__":
    test_chatbot()