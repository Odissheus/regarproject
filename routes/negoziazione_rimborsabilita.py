from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Dati di esempio per "Negoziazione e Rimborsabilità"
negoziazione_rimborsabilita_data = [
    {
        "id": 1,
        "titolo": "Negoziazione farmaci biologici",
        "descrizione": "Discussione sui nuovi accordi per i farmaci biologici.",
        "data_pubblicazione": datetime(2024, 9, 1).strftime("%Y-%m-%d"),
        "link": "https://www.aifa.gov.it/negoziazione-rimborsabilita"
    },
    {
        "id": 2,
        "titolo": "Modifiche alla rimborsabilità",
        "descrizione": "Aggiornamento delle condizioni di rimborsabilità per il 2024.",
        "data_pubblicazione": datetime(2024, 9, 15).strftime("%Y-%m-%d"),
        "link": "https://www.aifa.gov.it/negoziazione-rimborsabilita"
    }
]

@router.get("/negoziazione-rimborsabilita")
def get_negoziazione_rimborsabilita():
    return {"data": negoziazione_rimborsabilita_data}
