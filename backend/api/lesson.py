from fastapi import APIRouter, Depends
from core.user import UserFinancialProfile
from core.lesson import LessonService, LessonResponse
from typing import Annotated
from data.database import db

router = APIRouter(prefix="/lessons", tags=["lessons"])
DB = Annotated[db.SessionLocal, Depends(db.get_db)]


@router.post("/lesson", response_model=LessonResponse)
async def generate_lesson(context: UserFinancialProfile):
    lesson_service = LessonService()
    return await lesson_service.generate_lesson(context)


@router.put("/lesson")
async def save_lesson(transcript: str, user_profile_id: int, db: DB):
    Lesson_service = LessonService()
    try:
        return await Lesson_service.save_lesson(transcript, user_profile_id, db)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}
