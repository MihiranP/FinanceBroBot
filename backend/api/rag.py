from fastapi import APIRouter, Depends, HTTPException
from core.rag import RAG_Service
from data.database import db
from typing import Annotated
from visibility.logging import logger
from pydantic import BaseModel

router = APIRouter(prefix="/rag", tags=["rag"])
DB = Annotated[db.SessionLocal, Depends(db.get_db)]


class EmbedRequest(BaseModel):
    data_path: str


@router.post("/embed")
async def embed_df(request: EmbedRequest, db: DB):
    try:
        if db is None:
            raise HTTPException(
                status_code=500, detail="Database session not initialized"
            )

        rag_service = RAG_Service(db)
        rag_service.load_dataset(request.data_path)
        result = await rag_service.embed_df()
        return result
    except Exception as e:
        logger.error(f"Error embedding dataframe: {e}")
        if db is not None:
            db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
