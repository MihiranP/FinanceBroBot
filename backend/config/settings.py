from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    llm_api_base_url: str | None = os.getenv("LLM_API_BASE_URL")
    llm_model_name: str | None = os.getenv("LLM_MODEL_NAME")
    llm_api_key: str | None = os.getenv("LLM_API_KEY")
    postgres_db_name: str | None = os.getenv("POSTGRES_DB_NAME")
    postgres_db_user: str | None = os.getenv("POSTGRES_DB_USER")
    postgres_db_password: str | None = os.getenv("POSTGRES_DB_PASSWORD")
    postgres_db_host: str | None = os.getenv("POSTGRES_DB_HOST")
    postgres_db_port: str | None = os.getenv("POSTGRES_DB_PORT")
    log_level: str | None = os.getenv("LOG_LEVEL")


settings = Settings()
