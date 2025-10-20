"""
Streamlit UI for Hybrid Travel Assistant.
Combines AI reasoning + Neo4j graph visualization.
"""

import streamlit as st
from app.hybrid.hybrid_chat import HybridChat
from app.hybrid.hybrid_retriever import HybridRetriever
from pyvis.network import Network
import tempfile
import os
import nest_asyncio
import asyncio

# --- Fix Streamlit event loop issue ---
nest_asyncio.apply()
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# --- Page Config ---
st.set_page_config(
    page_title="Hybrid Travel Assistant 🌏",
    page_icon="🌴",
    layout="wide",
)

# --- Title ---
st.title("🌴 Hybrid Travel Assistant")
st.markdown(
    "Ask anything about Vietnam (or your travel dataset) — get intelligent, connected responses powered by **Pinecone + Neo4j + OpenAI.**"
)

# --- Initialize session state ---
if "chat" not in st.session_state:
    st.session_state.chat = HybridChat(enable_cache=True)

chat = st.session_state.chat
retriever = HybridRetriever()

# --- User Input ---
query = st.text_area(
    "Enter your travel query:",
    placeholder="e.g., Create a romantic 4-day itinerary in Vietnam 🌸",
    height=100,
)

col1, col2 = st.columns([1, 5])
with col1:
    run = st.button("✨ Generate Plan")

# --- Output Area ---
if run and query.strip():
    st.info("Fetching travel insights... please wait ⏳")

    try:
        # 1. Run hybrid reasoning
        result = chat.handle_query(query)
        answer = result.get("answer", "")
        matches = result.get("matches", [])
        facts = result.get("graph_facts", [])
        ts = result.get("timestamp", "")

        # 2. Display answer
        st.markdown(f"### 🧭 Travel Plan (Generated at {ts})")
        st.markdown(answer)

        # 3. Display quick summary
        try:
            summary = retriever.search_summary(result)
            st.markdown("### 🧩 Quick Summary")
            st.markdown(summary)
        except Exception as e:
            st.warning(f"⚠️ Could not generate summary: {e}")

        # 4. Graph visualization
        # 4. Graph visualization
        st.markdown("### 🌐 Knowledge Graph Visualization")
        if facts:
            try:
                net = Network(height="550px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
                net.force_atlas_2based(gravity=-30, spring_length=100)

                for fact in facts:
                    src = fact.get("source", "Unknown")
                    tgt = fact.get("target_name", "Unknown")
                    rel = fact.get("rel", "related_to")

                    net.add_node(src, label=src, color="#03A9F4")
                    net.add_node(tgt, label=tgt, color="#FF9800")
                    net.add_edge(src, tgt, label=rel)

                # ✅ FIX: use write_html instead of show()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
                    net.write_html(tmpfile.name)
                    with open(tmpfile.name, "r", encoding="utf-8") as f:
                        graph_html = f.read()

                st.components.v1.html(graph_html, height=600, scrolling=True)
                os.unlink(tmpfile.name)
            except Exception as e:
                st.warning(f"⚠️ Graph visualization error: {e}")
        else:
            st.info("No graph data found for this query.")


        # 5. Metadata expander
        with st.expander("🔍 Context Details"):
            st.write(f"**Semantic matches:** {len(matches)}")
            st.write(f"**Graph facts:** {len(facts)}")
            st.write(f"**Top match IDs:** {[m.get('id') for m in matches[:5]]}")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🧹 Clear Cache"):
        chat.clear_cache()
        st.success("Cache cleared!")

    if st.button("🔌 Close Connection"):
        chat.close()
        st.warning("Connection closed.")

st.markdown("---")
st.caption("💠 Powered by OpenAI + Pinecone + Neo4j | Built by Blue Enigma")
