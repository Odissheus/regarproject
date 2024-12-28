from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ListeTrasparenza

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_liste_trasparenza(db: Session = Depends(get_db)):
    return db.query(ListeTrasparenza).all()
