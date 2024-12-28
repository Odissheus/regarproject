from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ElenchiClasseAH

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_elenchi_classe_a_h(db: Session = Depends(get_db)):
    return db.query(ElenchiClasseAH).all()
