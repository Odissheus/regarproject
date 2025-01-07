from sqlalchemy import Column, Integer, String, Float, Date, Text
from database import Base

class PrezziRimborso(Base):
    __tablename__ = 'prezzi_rimborso'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    titolo = Column(String)
    link = Column(String)

class ListeTrasparenza(Base):
    __tablename__ = 'liste_trasparenza'
    id = Column(Integer, primary_key=True)
    principio_attivo = Column(String)
    nome_commerciale = Column(String)
    prezzo = Column(Float)
    data_aggiornamento = Column(Date)

class ModificaListaTrasparenza(Base):
    __tablename__ = 'modifiche_lista_trasparenza'
    id = Column(Integer, primary_key=True)
    data_modifica = Column(Date)
    tipo_modifica = Column(String)
    principio_attivo = Column(String)
    dettagli_modifica = Column(Text)