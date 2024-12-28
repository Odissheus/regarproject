from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import FarmaciInnovativi

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_farmaci_innovativi(db: Session = Depends(get_db)):
    return db.query(FarmaciInnovativi).all()
