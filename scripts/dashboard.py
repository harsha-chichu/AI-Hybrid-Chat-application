# scripts/dashboard.py
"""
Streamlit dashboard to view Neo4j graph visualization (generated HTML)
and basic system stats (cache size, retriever index list).

Run:
    streamlit run scripts/dashboard.py
"""

import os
import streamlit as st
from app.logger import get_logger
from app.hybrid.hybrid_chat import HybridChat
from app.retrievers.pinecone_retriever import PineconeRetriever

logger = get_logger(__name__)

st.set_page_config(page_title="Hybrid AI — Neo4j Graph", layout="wide")

st.title("Hybrid AI - Graph Visualization")

# Path to generated HTML
viz_path = "outputs/neo4j_viz.html"

if not os.path.exists(viz_path):
    st.warning("Visualization file not found. Generate it first with scripts/visualize_graph.py")
else:
    st.markdown("**Neo4j Graph Visualization**")
    with open(viz_path, "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=800, scrolling=True)

st.sidebar.header("System")
with st.sidebar:
    st.write("Pinecone index info")
    try:
        pr = PineconeRetriever()
        idxs = pr.pc.list_indexes().names()
        st.write("Available indexes:", idxs)
    except Exception as e:
        st.error(f"Pinecone access error: {e}")

    st.write("---")
    st.write("Hybrid Chat quick test")
    if st.button("Run sample query"):
        chat = HybridChat()
        q = "Suggest a 3-day itinerary in Hanoi"
        with st.spinner("Getting answer..."):
            res = chat.handle_query(q)
        st.markdown("**Answer**")
        st.write(res["answer"])
        st.markdown("**Matches & Facts**")
        st.write({"matches": len(res["matches"]), "graph_facts": len(res["graph_facts"])})
        chat.close()
