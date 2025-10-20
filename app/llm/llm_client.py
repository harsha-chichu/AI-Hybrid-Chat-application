"""
app/llm/llm_client.py
Handles all OpenAI API interactions: embeddings + chat completions.
Includes retry, timeout, and unified error handling.
"""

import logging
import time
from typing import List, Dict, Optional
from openai import OpenAI, APIError, RateLimitError, APITimeoutError
from app.config_loader import Config
from app.exceptions import LLMError

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper around OpenAI client for embeddings and chat completions.
    Provides unified error handling, retries, and logging.
    """

    def __init__(self):
        try:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            logger.info("✅ LLMClient initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize OpenAI client.")
            raise LLMError(f"OpenAI initialization failed: {e}")

    def _retry_request(self, func, max_retries: int = 3, delay: int = 3):
        """Generic retry wrapper for API calls."""
        for attempt in range(1, max_retries + 1):
            try:
                return func()
            except (RateLimitError, APITimeoutError) as e:
                logger.warning(f"[Retry {attempt}/{max_retries}] OpenAI API issue: {e}")
                time.sleep(delay * attempt)  # Exponential backoff
            except APIError as e:
                logger.warning(f"[Retry {attempt}/{max_retries}] Transient APIError: {e}")
                time.sleep(delay * attempt)
            except Exception as e:
                logger.exception("Unexpected LLM call failure.")
                raise LLMError(f"Unexpected LLM error: {e}")
        raise LLMError("Max retries reached for OpenAI request.")

    def embed_text(
        self,
        text: str,
        model: str = "text-embedding-3-small",
        timeout: Optional[int] = 30
    ) -> List[float]:
        """Return embedding vector for the given text."""
        try:
            def _embed_call():
                return self.client.embeddings.create(model=model, input=[text], timeout=timeout)

            resp = self._retry_request(_embed_call)
            embedding = resp.data[0].embedding
            logger.debug(f"Generated embedding (len={len(embedding)}).")
            return embedding
        except Exception as e:
            logger.exception("Embedding generation failed.")
            raise LLMError(f"Embedding failed: {e}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
        max_tokens: int = 2000,
        timeout: Optional[int] = 60
    ) -> str:
        """Return chat completion output from OpenAI."""
        try:
            def _chat_call():
                return self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=timeout
                )

            response = self._retry_request(_chat_call)
            content = response.choices[0].message.content
            logger.debug(f"Received chat response (len={len(content)}).")
            return content.strip()
        except Exception as e:
            logger.exception("ChatCompletion failed.")
            raise LLMError(f"ChatCompletion failed: {e}")


# Shared singleton instance
llm_client = LLMClient()

# Functional-style accessors for convenience
def embed_text(text: str) -> List[float]:
    return llm_client.embed_text(text)

def chat_completion(messages: List[Dict[str, str]]) -> str:
    return llm_client.chat_completion(messages)
