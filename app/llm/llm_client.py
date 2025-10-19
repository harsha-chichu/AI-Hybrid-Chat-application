"""
app/llm/llm_client.py
Handles all OpenAI API interactions: embeddings + chat completions.
"""

import logging
from typing import List, Dict
from openai import OpenAI
from app.config_loader import Config
from app.exceptions import LLMError

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper around OpenAI client for embeddings and chat completions.
    Provides unified error handling and logging.
    """

    def __init__(self):
        try:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            logger.info("LLMClient initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize OpenAI client.")
            raise LLMError(f"OpenAI initialization failed: {e}")

    def embed_text(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """Return embedding vector for the given text."""
        try:
            resp = self.client.embeddings.create(model=model, input=[text])
            embedding = resp.data[0].embedding
            logger.debug(f"Generated embedding of length {len(embedding)}.")
            return embedding
        except Exception as e:
            logger.exception("Embedding generation failed.")
            raise LLMError(f"Embedding failed: {e}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        max_tokens: int = 600,
    ) -> str:
        """Return chat completion output from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            logger.debug(f"Received chat response of length {len(content)}.")
            return content.strip()
        except Exception as e:
            logger.exception("ChatCompletion failed.")
            raise LLMError(f"ChatCompletion failed: {e}")


# Instantiate a shared singleton client for use across modules
llm_client = LLMClient()

# Functional-style shortcuts
def embed_text(text: str) -> List[float]:
    return llm_client.embed_text(text)

def chat_completion(messages: List[Dict[str, str]]) -> str:
    return llm_client.chat_completion(messages)
