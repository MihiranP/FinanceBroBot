from typing import Literal
from pydantic import BaseModel
from config.settings import settings
from openai import AsyncOpenAI
from visibility.logging import logger
import json


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Conversation(BaseModel):
    messages: list[Message] | None = []


class LLM_Hyperparameters(BaseModel):
    model: str = settings.llm_model_name
    temperature: float = 0.3
    max_tokens: int = 4096
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class LLM_API_Config(BaseModel):
    base_url: str = settings.llm_api_base_url
    api_key: str = settings.llm_api_key
    base_model: str = settings.llm_model_name


class LLM_Service:
    def __init__(
        self,
        llm_api_config: LLM_API_Config,
        llm_hyperparameters: LLM_Hyperparameters = LLM_Hyperparameters(),
    ):

        self.llm_api_config = llm_api_config
        self.llm_api_client: AsyncOpenAI = AsyncOpenAI(
            api_key=self.llm_api_config.api_key, base_url=self.llm_api_config.base_url
        )
        self.hyperparameters: LLM_Hyperparameters = llm_hyperparameters

    @property
    def hyperparameters(self):
        return self._hyperparameters

    @property
    def llm_api_client(self):
        return self._llm_api_client

    async def query(self, message: str, json_mode: bool = False):
        try:
            message = Message(role="user", content=message)
            logger.debug("Querying LLM with user message: {}", message.content)
            if json_mode:
                response = await self.llm_api_client.chat.completions.create(
                    model=self.hyperparameters.model,
                    messages=self.get_messages(),
                    temperature=self.hyperparameters.temperature,
                    max_tokens=self.hyperparameters.max_tokens,
                    top_p=self.hyperparameters.top_p,
                    frequency_penalty=self.hyperparameters.frequency_penalty,
                    presence_penalty=self.hyperparameters.presence_penalty,
                    response_format={"type": "json_object"},
                )
                response_json = json.loads(response.choices[0].message)
                logger.debug("LLM JSON response: {}", response_json)
                return response_json
            else:
                response = await self.llm_api_client.chat.completions.create(
                    model=self.hyperparameters.model,
                    messages=self.get_messages(),
                    temperature=self.hyperparameters.temperature,
                    max_tokens=self.hyperparameters.max_tokens,
                    top_p=self.hyperparameters.top_p,
                    frequency_penalty=self.hyperparameters.frequency_penalty,
                    presence_penalty=self.hyperparameters.presence_penalty,
                )
            logger.debug("LLM response: {}", response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            logger.exception(f"Error querying LLM: {e}")
            raise e
