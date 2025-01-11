from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.llm import Message, LLM_Service, LLM_API_Config
from visibility.logging import logger
from typing import Any

router = APIRouter(prefix="/llm", tags=["llm"])


class LLMQueryRequest(BaseModel):
    messages: list[Message]
    json_mode: bool | None = False


class LLMQueryResponse(BaseModel):
    response: Any


llm_service = LLM_Service(llm_api_config=LLM_API_Config())


@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest):
    """
    Query the LLM with a list of messages
    """
    try:
        response = await llm_service.query(
            messages=request.messages, json_mode=request.json_mode
        )
        return LLMQueryResponse(response=response)
    except Exception as e:
        logger.error(f"Error in LLM query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
