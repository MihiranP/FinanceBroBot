from pydantic import BaseModel
from config.settings import app_settings
from visibility.logging import logger
from llm import LLM_Service, LLM_API_Config
import pandas as pd


class RAGSettings(BaseModel):
    embedding_model_name: str = app_settings.embedding_model_name


class Embedding(BaseModel):
    content: str
    embedding: list[list[float]] | None = None


class Embeddings(BaseModel):
    embeddings: list[Embedding] | None = None


class RAG_Service:
    def __init__(
        self,
        rag_settings: RAGSettings = RAGSettings(),
        llm_config: LLM_API_Config = LLM_API_Config(),
        df: pd.DataFrame = None,
    ):
        self.rag_settings = rag_settings
        self.llm_service = LLM_Service(llm_api_config=llm_config)
        self.df = df
        self.embeddings: Embeddings | None = None

    def load_dataset(self, dataset_path: str):
        self.df = pd.read_csv(dataset_path)
        return self.df

    async def embed_set(self, text: str) -> Embedding:
        try:
            embedding = await self.llm_service.llm_api_client.embeddings.create(
                input=text,
                model=self.rag_settings.embedding_model_name,
            )
            return Embedding(
                content=text,
                embedding=embedding.data[0].embedding,
            )
        except Exception as e:
            logger.error(f"Error embedding text: {e}")
            raise e

    async def embed_df(self, df: pd.DataFrame) -> Embeddings:
        try:
            embeddings = []
            for index, row in df.iterrows():
                embedding = await self.embed_set(row["content"])
                embeddings.append(embedding)
            self.embeddings = Embeddings(embeddings=embeddings)
            return self.embeddings
        except Exception as e:
            logger.error(f"Error embedding dataframe: {e}")
            raise e
