from llm import LLM_Service, LLM_API_Config


class RAG_Service:
    def __init__(self, llm_config: LLM_API_Config = LLM_API_Config()):
        self.llm_service = LLM_Service(llm_api_config=llm_config)
