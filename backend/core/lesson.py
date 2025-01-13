from core.prompts import Prompts
from core.user import UserFinancialProfile
from core.llm import LLM_Service, Message, LLM_API_Config
from visibility.logging import logger
from pydantic import BaseModel
from data.schema import LessonPlans, UserProfile
from sqlalchemy.exc import SQLAlchemyError


class LessonSections(BaseModel):
    title: str
    content: str


class LessonResponse(BaseModel):
    plan: list[LessonSections]


class LessonService:
    """
    A class that generates lessons for a user.
    """

    def __init__(self, llm_api_config: LLM_API_Config = LLM_API_Config()):
        self.prompts = Prompts()
        self.llm_service = LLM_Service(llm_api_config=llm_api_config)

    async def generate_lesson(self, context: UserFinancialProfile) -> LessonResponse:
        """
        Generate a lesson for a user.
        """
        try:
            prompt = Message(
                role="user",
                content=self.prompts.LESSONPLAN_GENERATION_PROMPT.replace(
                    "{{context}}", context.convert_to_prompt_string()
                ).replace("{{name}}", context.name),
            )

            response = await self.llm_service.query([prompt], json_mode=True)
            logger.info(response)
            return LessonResponse(plan=response)
        except Exception as e:
            logger.exception(f"An error occurred while generating lesson: {e}")
            raise e

    async def save_lesson(self, transcript: str, user_profile_id: int, db):
        """
        Save lessons to the db
        """
        to_save = LessonPlans(user_profile_id=user_profile_id, transcript=transcript)
        user = (
            db.query(UserProfile)
            .filter(UserProfile.profile_id == user_profile_id)
            .first()
        )
        if not user:
            logger.error(
                "No user with associated user_id when creating lesson??? Manav what did you do?"
            )
        try:
            db.add(to_save)
            db.commit()
            db.refresh(to_save)
            return {
                "status": "success",
                "lesson_plan_id": to_save.lesson_plan_id,
                "user_profile_id": to_save.user_profile_id,
            }
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"An error occurred while saving lesson to the database: {e}")
            raise e
