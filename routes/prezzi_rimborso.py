from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import PrezziRimborso

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_prezzi_rimborso(db: Session = Depends(get_db)):
    return db.query(PrezziRimborso).all()
