from core.prompts import Prompts
from core.user import UserFinancialProfile
from core.llm import LLM_Service, Message, LLM_API_Config
from visibility.logging import logger
from pydantic import BaseModel


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
