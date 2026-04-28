from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse

from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    result = await llm_service.chat(request.message)
    return ChatResponse(answer=result["answer"], model=result["model"])
