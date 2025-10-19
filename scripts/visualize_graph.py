# scripts/visualize_graph.py
from neo4j import GraphDatabase
from pyvis.network import Network
import os
from app.config_loader import Config
from app.logger import get_logger

logger = get_logger(__name__)
OUTPUT_HTML = os.path.join("outputs", "neo4j_viz.html")
os.makedirs("outputs", exist_ok=True)

def fetch_subgraph(tx, limit=500):
    q = (
        "MATCH (a:Entity)-[r]->(b:Entity) "
        "RETURN a.id AS a_id, labels(a) AS a_labels, a.name AS a_name, "
        "b.id AS b_id, labels(b) AS b_labels, b.name AS b_name, type(r) AS rel "
        "LIMIT $limit"
    )
    return list(tx.run(q, limit=limit))

def build_pyvis(rows, output_html=OUTPUT_HTML):
    net = Network(height="900px", width="100%", directed=True, notebook=False)
    for rec in rows:
        a_id = rec["a_id"]; a_name = rec["a_name"] or a_id
        b_id = rec["b_id"]; b_name = rec["b_name"] or b_id
        a_labels = rec["a_labels"]; b_labels = rec["b_labels"]
        rel = rec["rel"]
        net.add_node(a_id, label=f"{a_name}\n({','.join(a_labels)})", title=f"{a_name}")
        net.add_node(b_id, label=f"{b_name}\n({','.join(b_labels)})", title=f"{b_name}")
        net.add_edge(a_id, b_id, title=rel)
    net.write_html(output_html, open_browser=False)
    logger.info(f"Saved visualization to {output_html}")

def main():
    driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
    rows = []
    try:
        with driver.session() as session:
            rows = session.execute_read(fetch_subgraph, limit=500)
    except Exception as e:
        logger.exception("Failed to fetch subgraph")
    build_pyvis(rows)

if __name__ == "__main__":
    main()
