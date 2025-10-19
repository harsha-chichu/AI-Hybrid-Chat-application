import logging
from typing import List, Dict
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from app.config_loader import Config
from app.exceptions import RetrievalError

logger = logging.getLogger(__name__)

class PineconeRetriever:
    """
    Handles semantic retrieval using Pinecone + OpenAIe embeddings.
    """

    def __init__(self):
        try:
            self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
            self.client = OpenAI(api_key = Config.OPENAI_API_KEY)
            self.index_name = Config.PINECONE_INDEX_NAME
            self.vector_dim = Config.PINECONE_VECTOR_DIM
            self._ensure_index_exists()
            self.index = self.pc.Index(self.index_name)
            logger.info(f"PineconeRetriever initialised (index: {self.index_name})")

        except Exception as e:
            logger.exception("Failed to initialize PineconeRetriever")
            raise RetrievalError(f"Error initializing PineconeRetriever: {e}")
        
    def _ensure_index_exists(self):
        """Ensure the index exists or create it if missing."""
        existing_indexes = self.pc.list_indexes().names()
        if self.index_name not in existing_indexes:
            logger.warning(f"Index {self.index_name} not found. Creating new one.")
            self.pc.create_index(
                name = self.index_name,
                dimension = self.vector_dim,
                metric = "cosine",
                spec = ServerlessSpec(cloud = "aws", region = "us-east1-gcp")
            )
    
    def get_embedding(self, text: str, model = "text-embedding-3-small") -> List[float]:
        """Generate an embedding for a given text."""
        try:
            response = self.client.embeddings.create(model = model, input = [text])
            return response.data[0].embedding
        
        except Exception as e:
            logger.exception("Error generate embedding.")
            raise RetrievalError(f"Failed to embed text: {e}")
        
    def query(self, text: str, top_k: int = Config.TOP_K) -> List[Dict]:
        """Query Pinecone for the most similar items."""
        try:
            vector = self.get_embedding(text)
            results = self.index.query(
                vector = vector,
                top_k = top_k,
                include_metadata = True,
                include_values = False,
            )
            matches = results.get("matches", [])
            logger.info(f"Pinecone query returned {len(matches)} matches.")
            return matches
            

        except Exception as e:
            logger.exception("Error during Pinecone query.")
            raise RetrievalError(f"Pinecone query failed: {e}")