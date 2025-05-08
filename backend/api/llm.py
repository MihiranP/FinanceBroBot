from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from core.llm import Message, LLM_Service, LLM_API_Config
from core.rag import RAG_Service
from data.database import db
from visibility.logging import logger
from typing import Annotated, Any

router = APIRouter(prefix="/llm", tags=["llm"])
DB = Annotated[db.SessionLocal, Depends(db.get_db)]


class LLMQueryRequest(BaseModel):
    messages: list[Message]
    json_mode: bool | None = False
    rag_enabled: bool | None = False


class LLMQueryResponse(BaseModel):
    response: Any


llm_service = LLM_Service(llm_api_config=LLM_API_Config())


@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest, db: DB):
    """
    Query the LLM with a list of messages
    """
    try:
        context = None
        if request.rag_enabled:
            rag_service = RAG_Service(db)
            context = await rag_service.get_top_k_embeddings(
                request.messages[-1].content, 5
            )
            context = "\n\n".join(context)
            logger.debug(f"RAG context pulled: {context}")
        response = await llm_service.query(
            messages=request.messages,
            json_mode=request.json_mode,
            rag_context=context,
        )
        return LLMQueryResponse(response=response)
    except Exception as e:
        logger.error(f"Error in LLM query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
