from .LLMEnums import LLMEnums
from .providers import OpenAiProvider, CoHereProvider, GoogleProvider


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAiProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.OPENAI_DEFAULT_INPUT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.OPENAI_DEFAULT_OUTPUT_MAX_TOKENS,
                default_temperature=self.config.OPENAI_DEFAULT_TEMPERATURE,
            )

        elif provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.COHERE_DEFAULT_INPUT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.COHERE_DEFAULT_OUTPUT_MAX_TOKENS,
                default_temperature=self.config.COHERE_DEFAULT_TEMPERATURE,
            )

        elif provider == LLMEnums.GEMINI.value:
            return GoogleProvider(
                api_key=self.config.GOOGLE_API_KEY,
                default_input_max_characters=self.config.GEMINI_DEFAULT_INPUT_MAX_CHARACTERS,
                default_output_max_characters=self.config.GEMINI_DEFAULT_OUTPUT_MAX_TOKENS,
                default_generation_temperature=self.config.GEMINI_DEFAULT_TEMPERATURE,
            )
        return None
