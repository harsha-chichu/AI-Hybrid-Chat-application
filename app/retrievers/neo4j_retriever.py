import logging
from typing import List, Dict
from neo4j import GraphDatabase
from app.config_loader import Config
from app.exceptions import GraphError

logger = logging.getLogger(__name__)

class Neo4jRetriever:
    """
    Fetches contextual graph facts from Neo4j.
    """

    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
            )
            logger.info("Neo4jRetriever initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize Neo4jRetriever.")
            raise GraphError(f"Error connecting to Neo4j: {e}")
        
    def fetch_neighbors(self, node_ids: List[str], limit_per_node: int = 10) -> List[Dict]:
        """
        Fetch neighboring nodes and relationships for each input node ID.
        Returns a list of facts (edges) describing the relationships.
        """
        if not node_ids:
            logger.warning("No node IDs provided for graph retrieval.")
            return []

        facts = []
        try:
            with self.driver.session() as session:
                for nid in node_ids:
                    q = (
                        "MATCH (n:Entity {id:$nid})-[r]-(m:Entity) "
                        "RETURN type(r) AS rel, labels(m) AS labels, "
                        "m.id AS id, m.name AS name, m.type AS type, "
                        "m.description AS description "
                        "LIMIT $limit"
                    )
                    results = session.run(q, nid=nid, limit=limit_per_node)
                    for r in results:
                        facts.append({
                            "source": nid,
                            "rel": r["rel"],
                            "target_id": r["id"],
                            "target_name": r["name"],
                            "target_desc": (r["description"] or "")[:400],
                            "labels": r["labels"]
                        })
                logger.info(f"Fetched {len(facts)} graph facts for {len(node_ids)} nodes.")
            return facts

        except Exception as e:
            logger.exception("Graph retrieval failed.")
            raise GraphError(f"Failed to fetch graph context: {e}")
        
    def fetch_graph_context(self, node_ids):
        """
        Compatibility wrapper for HybridRetriever.
        Delegates to fetch_neighbors().
        """
        try:
            return self.fetch_neighbors(node_ids)
        except Exception as e:
            logger.exception("Graph context fetch failed.")
            raise GraphError(f"Graph context fetch failed: {e}")
        
    def close(self):
        """Close the Neo4j driver connection."""
        try:
            self.driver.close()
            logger.info("Neo4j connection closed.")
        except Exception as e:
            logger.warning(f"Error closing Neo4j connection: {e}")
