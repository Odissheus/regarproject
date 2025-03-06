from typing import List, Dict
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import ListeTrasparenza, PrezziRimborso
from datetime import datetime
from scraper import scrape_aifa_news

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["https://regarproject.netlify.app", "https://regarproject.com", "http://localhost:3000"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

class PrezzoResponse(BaseModel):
   data: str
   titolo: str
   link: str
   
   class Config:
       orm_mode = True

class ListaResponse(BaseModel):
   principio_attivo: str
   nome_commerciale: str
   prezzo: float
   data_aggiornamento: str
   
   class Config:
       orm_mode = True

class NewsResponse(BaseModel):
   id: int
   date: str
   title: str
   summary: str
   link: str

class ChatbotRequest(BaseModel):
   query: str

class ChatbotResponse(BaseModel):
   response: str

@app.get("/")
def read_root():
    return {"message": "RegAr.AI API è online"}

@app.get("/prezzi-rimborso", response_model=List[PrezzoResponse])
def get_prezzi_rimborso(db: Session = Depends(get_db)):
   return db.query(PrezziRimborso).all()

@app.get("/liste-trasparenza", response_model=List[ListaResponse])
def get_liste_trasparenza(db: Session = Depends(get_db)):
   return db.query(ListeTrasparenza).all()

@app.get("/aifa-news", response_model=List[NewsResponse])
def get_aifa_news():
    """Recupera le ultime news dal sito AIFA"""
    try:
        news_items = scrape_aifa_news()
        
        if not news_items:
            # In caso di errore, restituisci dati statici di esempio
            return [
                {
                    "id": 1,
                    "date": datetime.now().isoformat(),
                    "title": "Esempio News AIFA 1",
                    "summary": "Questa è una news di esempio. Il servizio di scraping potrebbe non essere disponibile.",
                    "link": "https://www.aifa.gov.it/news"
                },
                {
                    "id": 2,
                    "date": datetime.now().isoformat(),
                    "title": "Esempio News AIFA 2",
                    "summary": "Questa è un'altra news di esempio. Il servizio di scraping potrebbe non essere disponibile.",
                    "link": "https://www.aifa.gov.it/news"
                }
            ]
        
        return news_items
    except Exception as e:
        print(f"Errore nel recupero delle news: {e}")
        # In caso di errore, restituisci dati statici
        return [
            {
                "id": 1,
                "date": datetime.now().isoformat(),
                "title": "Esempio News AIFA 1",
                "summary": "Questa è una news di esempio. Il servizio di scraping potrebbe non essere disponibile.",
                "link": "https://www.aifa.gov.it/news"
            }
        ]

@app.post("/chatbot", response_model=ChatbotResponse)
def chatbot_query(request: ChatbotRequest):
   """Processa una query per il chatbot AIFA"""
   query = request.query
   
   # Versione semplificata per iniziare
   # In produzione, implementare una vera integrazione con un modello di linguaggio
   response = ""
   
   # Risposte predefinite basate su parole chiave
   if "news" in query.lower() or "novità" in query.lower() or "ultime" in query.lower():
       response = """Ecco le ultime novità da AIFA:
       
1. Sono stati pubblicati nuovi aggiornamenti sulle liste di trasparenza
2. È disponibile la nuova circolare sui farmaci equivalenti
3. È stata aggiornata la procedura di farmacovigilanza

Puoi trovare maggiori dettagli sul sito ufficiale AIFA: [Sito AIFA](https://www.aifa.gov.it/)"""
   
   elif "farmaci" in query.lower() or "equivalenti" in query.lower() or "generici" in query.lower():
       response = """I farmaci equivalenti (o generici) sono farmaci che contengono lo stesso principio attivo, nella stessa quantità e con la stessa forma farmaceutica del medicinale di marca (originatore).

Puoi trovare le liste complete dei farmaci equivalenti sul sito AIFA nella sezione dedicata: [Liste di Trasparenza](https://www.aifa.gov.it/liste-di-trasparenza)

Se hai bisogno di informazioni su un farmaco specifico, puoi indicarmi il nome e cercherò di fornirti maggiori dettagli."""
   
   elif "farmacovigilanza" in query.lower() or "effetti collaterali" in query.lower() or "reazione" in query.lower():
       response = """La farmacovigilanza è l'insieme delle attività di monitoraggio degli effetti avversi dei farmaci.

Se desideri segnalare una reazione avversa, puoi:
1. Utilizzare il portale online: [VigiFarmaco](https://www.vigifarmaco.it/)
2. Contattare il Responsabile di Farmacovigilanza della tua ASL
3. Rivolgerti al tuo medico o farmacista

Per maggiori informazioni visita la sezione: [Farmacovigilanza AIFA](https://www.aifa.gov.it/farmacovigilanza)"""
   
   elif "carenze" in query.lower() or "indisponibile" in query.lower() or "mancanza" in query.lower():
       response = """AIFA pubblica regolarmente aggiornamenti sulle carenze di medicinali. 

Puoi trovare l'elenco completo dei farmaci carenti o temporaneamente indisponibili sul sito AIFA:
[Carenze e indisponibilità](https://www.aifa.gov.it/farmaci-carenti)

Se stai cercando un'alternativa a un farmaco non disponibile, consulta il tuo medico o farmacista."""
   
   else:
       response = """Sono l'assistente virtuale specializzato in informazioni sul sito AIFA.

Posso aiutarti a trovare informazioni su:
- Farmaci e liste di trasparenza
- Procedure di farmacovigilanza
- Normative e circolari
- Carenze di medicinali
- Ultime news e aggiornamenti

Se hai una domanda specifica, prova a formulare la tua richiesta in modo più dettagliato."""
   
   return ChatbotResponse(response=response)