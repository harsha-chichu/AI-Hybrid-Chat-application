import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
    """Centralized configuration loader."""
    
    # Neo4j
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Pinecone
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    PINECONE_VECTOR_DIM = int(os.getenv("PINECONE_VECTOR_DIM"))

    # Retrieval settings
    TOP_K = int(os.getenv("TOP_K", 5))

    @classmethod
    def sanity_check(cls):
        """Prints key configuration for debugging."""
        print("NEO4J_URI:", bool(cls.NEO4J_URI))
        print("OPENAI_KEY set:", bool(cls.OPENAI_API_KEY))
        print("TOP_K:", cls.TOP_K)
