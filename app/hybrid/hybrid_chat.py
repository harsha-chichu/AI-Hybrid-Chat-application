"""
HybridChat orchestrates retrieval from Pinecone and Neo4j,
builds prompts, and queries OpenAI’s chat model for reasoning.
"""

import logging
from typing import List, Dict
from app.retrievers.pinecone_retriever import PineconeRetriever
from app.retrievers.neo4j_retriever import Neo4jRetriever
from app.llm.llm_client import embed_text, chat_completion
from app.llm.prompt_builder import PromptBuilder
from app.exceptions import RetrievalError, LLMError

logger = logging.getLogger(__name__)

class HybridChat:
    """
    The reasoning orchestrator that merges vector + graph context
    for intelligent conversational responses.
    """

    def __init__(self):
        self.pinecone = PineconeRetriever()
        self.neo4j = Neo4jRetriever()
        self.prompt_builder = PromptBuilder()
        logger.info("HybridChat initialized.")

    def handle_query(self, query: str, top_k: int = 5) -> Dict:
        """End-to-end reasoning pipeline."""
        try:
            logger.info(f"Handling user query: {query}")

            # 1. Semantic retrieval
            matches = self.pinecone.query(query, top_k=top_k)
            match_ids = [m["id"] for m in matches]
            logger.info(f"Retrieved {len(matches)} semantic matches.")

            # 2. Graph context
            graph_facts = self.neo4j.fetch_graph_context(match_ids)
            logger.info(f"Retrieved {len(graph_facts)} graph facts.")

            # 3. Prompt creation
            messages = self.prompt_builder.build_prompt(query, matches, graph_facts)

            # 4. LLM reasoning
            answer = chat_completion(messages)

            # 5. Final structured output
            return {
                "query": query,
                "matches": matches,
                "graph_facts": graph_facts,
                "answer": answer,
            }

        except (RetrievalError, LLMError) as e:
            logger.error(f"Known error: {e}")
            raise
        except Exception as e:
            logger.exception("Hybrid reasoning failed.")
            raise RetrievalError(f"Hybrid reasoning failed: {e}")

    def close(self):
        """Clean up resources."""
        self.neo4j.close()
