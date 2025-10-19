class AppError(Exception):
    """Base class for all custom exceptions in the app."""
    pass


class ConfigError(AppError):
    """Raised when configuration loading fails."""
    pass


class RetrievalError(AppError):
    """Raised when a retriever (Pinecone/Neo4j) operation fails."""
    pass


class LLMError(AppError):
    """Raised when the LLM call fails."""
    pass


class GraphError(AppError):
    """Raised for Neo4j graph-related issues."""
    pass
