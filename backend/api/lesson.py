from fastapi import APIRouter
from core.user import UserFinancialProfile
from core.lessonplan import LessonService, LessonResponse

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/lesson", response_model=LessonResponse)
async def generate_podcast(context: UserFinancialProfile):
    lesson_service = LessonService()
    return await lesson_service.generate_lesson(context)
