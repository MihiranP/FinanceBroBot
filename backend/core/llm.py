from typing import Literal
from pydantic import BaseModel
from config.settings import app_settings
from openai import AsyncOpenAI
from visibility.logging import logger
import json
from tenacity import retry, stop_after_attempt, wait_exponential


class Message(BaseModel):
    role: Literal["user", "system", "assistant"]
    content: str


class LLM_Hyperparameters(BaseModel):
    model: str = app_settings.llm_model_name
    temperature: float = 0.3
    max_tokens: int = 4096
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class LLM_API_Config(BaseModel):
    base_url: str = app_settings.llm_api_base_url
    api_key: str = app_settings.llm_api_key
    base_model: str = app_settings.llm_model_name


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

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15)
    )
    async def query(
        self,
        messages: list[Message],
        json_mode: bool = False,
        rag_context: str | None = None,
    ):
        try:
            logger.debug("Querying LLM with latest message: {}", messages[-1])
            if rag_context is not None:
                ctx = messages[-1].content
                messages[-1].content = rag_context + ctx
            if json_mode:
                response = await self.llm_api_client.chat.completions.create(
                    model=self.hyperparameters.model,
                    messages=messages,
                    temperature=self.hyperparameters.temperature,
                    max_tokens=self.hyperparameters.max_tokens,
                    top_p=self.hyperparameters.top_p,
                    frequency_penalty=self.hyperparameters.frequency_penalty,
                    presence_penalty=self.hyperparameters.presence_penalty,
                    response_format={"type": "json_object"},
                )
                response_json = json.loads(response.choices[0].message.content)
                logger.debug("LLM JSON response: {}", response_json)
                return response_json
            else:
                llm_response = await self.llm_api_client.chat.completions.create(
                    model=self.hyperparameters.model,
                    messages=messages,
                    temperature=self.hyperparameters.temperature,
                    max_tokens=self.hyperparameters.max_tokens,
                    top_p=self.hyperparameters.top_p,
                    frequency_penalty=self.hyperparameters.frequency_penalty,
                    presence_penalty=self.hyperparameters.presence_penalty,
                )
            response = llm_response.choices[0].message.content
            logger.debug("LLM response: {}", response)
            return response
        except Exception as e:
            logger.exception(f"Error querying LLM: {e}")
            raise e
