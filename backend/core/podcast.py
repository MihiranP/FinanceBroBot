from core.prompts import Prompts
from core.user import UserFinancialProfile
from core.llm import LLM_Service, Message, LLM_API_Config
from visibility.logging import logger
from pydantic import BaseModel


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
