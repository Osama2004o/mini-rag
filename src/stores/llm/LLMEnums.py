from enum import Enum


class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    GEMINI = "GEMINI"


class OpenAiEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    CHATBOT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentType(Enum):
    DOCUMENT = "document"
    QUERY = "query"
