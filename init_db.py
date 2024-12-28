# init_db.py
from models import Base
from database import engine

def init_database():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_database()