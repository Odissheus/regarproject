from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import PrezziRimborso, ListeTrasparenza 
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["https://regarproject.netlify.app", "http://localhost:3000"],
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

@app.get("/prezzi-rimborso", response_model=List[PrezzoResponse])
def get_prezzi_rimborso(db: Session = Depends(get_db)):
   return db.query(PrezziRimborso).all()

@app.get("/liste-trasparenza", response_model=List[ListaResponse])
def get_liste_trasparenza(db: Session = Depends(get_db)):
   return db.query(ListeTrasparenza).all()