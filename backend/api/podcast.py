from fastapi import APIRouter, Depends
from core.user import UserFinancialProfile
from core.podcast import PodcastService, PodcastResponse
from typing import Annotated
from data.database import db

router = APIRouter(prefix="/podcasts", tags=["podcasts"])
DB = Annotated[db.SessionLocal, Depends(db.get_db)]


@router.post("/podcast", response_model=PodcastResponse)
async def generate_podcast(context: UserFinancialProfile):
    podcast_service = PodcastService()
    return await podcast_service.generate_podcast(context)


@router.put("/save/podcast")
async def save_podcast(transcript: str, user_profile_id: int, db: DB):
    podcast_service = PodcastService()
    try:
        return await podcast_service.save_podcast(transcript, user_profile_id, db)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}
