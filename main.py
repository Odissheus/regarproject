# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import PrezziRimborso, ValutazioniEconomiche, RegistriMonitoraggio, NoteAifa, ElenchiClasseAH, FarmaciInnovativi, ListeTrasparenza

app = FastAPI()

@app.get("/prezzi-rimborso")
def get_prezzi_rimborso(db: Session = Depends(get_db)):
    return db.query(PrezziRimborso).all()

@app.get("/liste-trasparenza")
def get_liste_trasparenza(db: Session = Depends(get_db)):
    return db.query(ListeTrasparenza).all()

# altri endpoint rimanenti...