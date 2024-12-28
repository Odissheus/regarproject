from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from chat_manager import ChatManager

router = APIRouter()
chat_manager = ChatManager()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def get_chat_response(request: ChatRequest):
    try:
        response = chat_manager.get_response(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))