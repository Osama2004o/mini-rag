from stores.llm.LLMInterface import LLMInterface
from stores.llm.LLMEnums import GeminiEnums
from google import genai
import logging


class GoogleProvider(LLMInterface):
    def __init__(
        self,
        api_key: str,
        api_url: str = None,
        default_input_max_characters: int = 1000,
        default_output_max_characters: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_characters = default_output_max_characters
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = genai.Client(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generatino_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[: self.default_input_max_characters].strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: list = [],
        max_output_token: int = None,
        temperature: float = None,
    ):
        if not self.client:
            self.logger.error("Google Client not initialized")
            return None

        if not self.generatino_model_id:
            self.logger.error("Generation model for Google not set")
            return None

        max_output_token = max_output_token or self.default_output_max_characters
        temperature = temperature or self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(
                prompt=prompt,
                role=GeminiEnums.USER.value,
            )
        )

        response = self.client.models.generate_content(
            model=self.generatino_model_id,
            contents=chat_history,
            config={
                "max_output_tokens": max_output_token,
                "temperature": temperature,
            },
        )

        if not response or not response.candidates or len(response.candidates) == 0:
            self.logger.error("Error while generating text with Google")
            return None

        return response.text

    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("Google Client not initialized")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Google not set")
            return None

        response = self.client.models.embed_content(
            model=self.embedding_model_id,
            contents=text,
        )

        if (
            not response
            or not response.embeddings
            or len(response.embeddings) == 0
        ):
            self.logger.error("Error while embedding text with Google")
            return None

        return response.embeddings[0].values

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "parts": [self.process_text(prompt)],
        }
