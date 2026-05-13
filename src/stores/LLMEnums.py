from enum import Enum


class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    GEMINI = "GEMINI"

class OpenAiEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
