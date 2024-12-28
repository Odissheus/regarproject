# models.py
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

class ValutazioniEconomiche(Base):
    __tablename__ = 'valutazioni_economiche'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    titolo = Column(String)
    link = Column(String)

class RegistriMonitoraggio(Base):
    __tablename__ = 'registri_monitoraggio'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    titolo = Column(String)
    link = Column(String)

class NoteAifa(Base):
    __tablename__ = 'note_aifa'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    titolo = Column(String)
    link = Column(String)

class ElenchiClasseAH(Base):
    __tablename__ = 'elenchi_classe_ah'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    titolo = Column(String)
    link = Column(String)

class FarmaciInnovativi(Base):
    __tablename__ = 'farmaci_innovativi'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    titolo = Column(String)
    link = Column(String)