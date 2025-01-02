from bs4 import BeautifulSoup
import requests
import PyPDF2
import io
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

Base = declarative_base()

class ListeTrasparenza(Base):
    __tablename__ = 'liste_trasparenza'
    
    id = Column(Integer, primary_key=True)
    principio_attivo = Column(String)
    nome_commerciale = Column(String)
    produttore = Column(String)
    dosaggio = Column(String)
    confezione = Column(String)
    prezzo = Column(Float)
    prezzo_riferimento = Column(Float)
    data_aggiornamento = Column(Date)

def scarica_pdf(url):
    response = requests.get(url)
    return io.BytesIO(response.content)

def analizza_lista_trasparenza_pdf(pdf_buffer):
    reader = PyPDF2.PdfReader(pdf_buffer)
    dati = []
    
    for pagina in reader.pages:
        testo = pagina.extract_text()
        # Analizza il testo in dati strutturati usando regex o operazioni stringa
        righe = analizza_testo_pdf(testo)
        dati.extend(righe)
    
    return dati

def scarica_liste_trasparenza():
    url = "https://www.aifa.gov.it/liste-di-trasparenza"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    link_pdf = []
    # Trova i link PDF nella pagina
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'Lista_farmaci_equivalenti' in href and href.endswith('.pdf'):
            link_pdf.append(href)
    
    tutti_dati = []
    for pdf_url in link_pdf:
        pdf_buffer = scarica_pdf(pdf_url)
        dati = analizza_lista_trasparenza_pdf(pdf_buffer)
        tutti_dati.extend(dati)
    
    return tutti_dati

def salva_nel_database(dati):
    engine = create_engine('sqlite:///liste_trasparenza.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        for elemento in dati:
            record = ListeTrasparenza(**elemento)
            session.add(record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def cerca_principio_attivo(principio):
    engine = create_engine('sqlite:///liste_trasparenza.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        risultati = session.query(ListeTrasparenza).filter(
            ListeTrasparenza.principio_attivo.ilike(f'%{principio}%')
        ).all()
        return risultati
    finally:
        session.close()

if __name__ == "__main__":
    dati = scarica_liste_trasparenza()
    salva_nel_database(dati)