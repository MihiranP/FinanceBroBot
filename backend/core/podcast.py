from core.prompts import Prompts
from core.user import UserFinancialProfile
from core.llm import LLM_Service, Message, LLM_API_Config
from visibility.logging import logger
from pydantic import BaseModel
from data.schema import Podcasts, UserProfile
from sqlalchemy.exc import SQLAlchemyError


class PodcastMessage(BaseModel):
    role: str
    content: str


class PodcastResponse(BaseModel):
    messages: list[PodcastMessage]


class PodcastService:
    """
    A class that generates podcasts for a user.
    """

    def __init__(self, llm_api_config: LLM_API_Config = LLM_API_Config()):
        self.prompts = Prompts()
        self.llm_service = LLM_Service(llm_api_config=llm_api_config)

    async def generate_podcast(
        self, context: UserFinancialProfile
    ) -> list[PodcastMessage]:
        """
        Generate a podcast for a user.
        """
        try:
            prompt = Message(
                role="user",
                content=self.prompts.PODCAST_TRANSCRIPTION_PROMPT.replace(
                    "{{context}}", context.convert_to_prompt_string()
                ).replace("{{name}}", context.name),
            )

            response = await self.llm_service.query([prompt], json_mode=True)
            return PodcastResponse(messages=response)
        except Exception as e:
            logger.exception(f"An error occurred while generating podcast: {e}")
            raise e

    async def generate_podcast_audio(
        self, podcast_messages: list[PodcastMessage]
    ) -> str:
        """
        Generate audio for a podcast.
        """
        pass

    async def save_podcast(self, transcript: str, user_profile_id: int, db):
        """
        Save the podcast to the database.
        """
        to_save = Podcasts(user_profile_id=user_profile_id, transcript=transcript)
        user = (
            db.query(UserProfile)
            .filter(UserProfile.profile_id == user_profile_id)
            .first()
        )
        if not user:
            logger.error(
                "No user with associated user_id when creating podcast??? Manav what did you do?"
            )
        try:
            db.add(to_save)
            db.commit()
            db.refresh(to_save)
            return {
                "status": "success",
                "podcast_id": to_save.podcast_id,
                "user_profile_id": to_save.user_profile_id,
            }
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"An error occurred while saving podcast to the database: {e}")
            raise e
