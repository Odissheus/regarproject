from fastapi import APIRouter
from pydantic import BaseModel

# Modello per la richiesta
class ChatbotRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/")
def chatbot(request: ChatbotRequest):
    return {"response": f"Simulazione risposta per la query: {request.query}"}
