"""
Hybrid Retriever - Combines Pinecone (semantic) + Neo4j (graph-based) retrievals.
"""

from typing import Dict, Any
from app.logger import get_logger
from app.retrievers.pinecone_retriever import PineconeRetriever
from app.retrievers.neo4j_retriever import Neo4jRetriever
from app.exceptions import RetrievalError

logger = get_logger(__name__)

class HybridRetriever:
    """Combines vector and graph retrieval for hybrid knowledge grounding."""

    def __init__(self):
        self.pinecone_retriever = PineconeRetriever()
        self.neo4j_retriever = Neo4jRetriever()
        logger.info("HybridRetriever initialized.")

    def retrieve(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Perform hybrid retrieval combining Pinecone + Neo4j."""
        try:
            # Step 1 — Vector retrieval
            matches = self.pinecone_retriever.query(query, top_k=top_k)
            match_ids = [m["id"] for m in matches if "id" in m]
            logger.info(f"Retrieved {len(matches)} semantic matches.")

            # Step 2 — Graph retrieval
            graph_facts = self.neo4j_retriever.fetch_graph_context(match_ids)
            logger.info(f"Retrieved {len(graph_facts)} graph facts.")

            # Step 3 — Merge both
            result = {
                "query": query,
                "semantic_matches": matches,
                "graph_facts": graph_facts,
                "summary": f"{len(matches)} semantic matches, {len(graph_facts)} graph facts"
            }

            return result

        except Exception as e:
            logger.exception("Hybrid retrieval failed.")
            raise RetrievalError(f"Hybrid retrieval failed: {e}")
        
    def search_summary(self, result: Dict, max_items: int = 5) -> str:
        """
        Generate a simple textual summary of top retrieved nodes and relationships.
        Useful for quick inspection or debugging.
        """
        if not result:
            return "No results to summarize."

        matches = result.get("matches", [])
        graph_facts = result.get("graph_facts", [])

        summary_lines = []
        summary_lines.append("**Search Summary:**")

        # Summarize top semantic matches
        summary_lines.append("\n**Top Semantic Matches:**")
        for m in matches[:max_items]:
            meta = m.get("metadata", {})
            name = meta.get("name", "Unknown")
            etype = meta.get("type", "Entity")
            desc = meta.get("description", "")[:100].strip()
            summary_lines.append(f"- {name} ({etype}): {desc}...")

        # Summarize graph relationships
        if graph_facts:
            summary_lines.append("\n**Graph Relationships (sample):**")
            for f in graph_facts[:max_items]:
                src = f.get("source", "Unknown")
                rel = f.get("rel", "related_to")
                tgt = f.get("target_name", "Unknown")
                summary_lines.append(f"- {src} —[{rel}]→ {tgt}")

        return "\n".join(summary_lines)
