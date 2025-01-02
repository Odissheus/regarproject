from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import PrezziRimborso, ListeTrasparenza
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/prezzi-rimborso", response_model=List[PrezzoResponse])
def get_prezzi_rimborso(db: Session = Depends(get_db)):
    return db.query(PrezziRimborso).all()

@app.get("/liste-trasparenza", response_model=List[ListaResponse])
def get_liste_trasparenza(db: Session = Depends(get_db)):
    return db.query(ListeTrasparenza).all()