# Hybrid AI Travel Assistant — Blue Enigma Challenge 🚀

This project implements a sophisticated **hybrid retrieval and reasoning** travel assistant. It combines the strengths of a graph database for structured data and a vector database for semantic understanding, orchestrated by a large language model to provide intelligent, context-aware travel recommendations.

---

## 📋 Table of Contents

- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Quickstart Guide](#quickstart-guide)
- [Design Rationale: Why Hybrid Retrieval?](#design-rationale-why-hybrid-retrieval)
- [Scaling, Reliability, and Maintenance](#scaling-reliability-and-maintenance)
- [Future-Proofing and Extensibility](#future-proofing-and-extensibility)

---

## ✨ Key Features

* **Hybrid Retrieval:** Leverages **Neo4j** for structured relationship queries (routes, connections) and **Pinecone** for semantic search over unstructured text, providing more accurate and grounded results.
* **Intelligent Reasoning:** Uses **OpenAI GPT models** to synthesize information from both retrieval sources, plan itineraries, and generate natural language responses.
* **Asynchronous & Non-Blocking I/O:** Built with `asyncio` and `run_in_executor` to ensure that blocking database and API calls do not freeze the application, enabling high concurrency.
* **Efficient Orchestration:** Implements a parallel retrieval strategy where semantic results from Pinecone are used to kickstart parallel graph retrievals from Neo4j.
* **Robust Error Handling:** Features custom exception classes, graceful fallbacks (e.g., to a single retriever if one is down), and automatic retries with exponential backoff for API calls.
* **Optimized Prompt Engineering:** A dynamic `PromptBuilder` organizes retrieved context by type and intelligently trims it to prevent token overflow and improve LLM focus.
* **Developer Tooling:** Includes scripts for data loading, an interactive command-line interface (CLI) for testing, and a Streamlit dashboard for graph visualization.

---

## 💻 Technology Stack

* **Graph Database:** Neo4j
* **Vector Database:** Pinecone
* **LLM & Embeddings:** OpenAI (GPT models)
* **Core Language:** Python
* **Developer Tools:** Streamlit, PyVis

---

## 🏗️ Architecture

The application is built with a modular and decoupled architecture to ensure maintainability and scalability.

* **app/retrievers/:** Contains dedicated connectors for Pinecone (semantic search) and Neo4j (graph traversal).
* **app/llm/:** A centralized client for interacting with the OpenAI API, complete with a `PromptBuilder` to structure context for the model.
* **app/hybrid/:** The core orchestration layer that combines the outputs from the retrievers, manages caching, and passes the final context to the LLM for reasoning and response generation.

This design separates data retrieval, LLM interaction, and business logic, making the system easier to test, debug, and extend.

---

## 📁 Project Structure

```
hybrid_ai_travel_assistant/
│
├── app/                  # Core application logic
│   ├── retrievers/       # Data retrieval modules (Pinecone, Neo4j)
│   ├── llm/              # LLM interaction layer (OpenAI client, prompt builder)
│   ├── hybrid/           # Orchestration logic for hybrid chat
│   └── utils/            # Miscellaneous helpers
│
├── scripts/              # Command-line tools for developers
│   ├── load_to_neo4j.py
│   ├── upload_to_pinecone.py
│   ├── visualize_graph.py
│   └── chat_cli.py       # Interactive chat CLI
│
├── data/                 # Data assets
│   └── vietnam_travel_dataset.json
│
├── config/               # Configuration constants
│   └── config.py
│
├── tests/                # Unit & integration tests
├── logs/                 # Runtime logs
├── docs/                 # Detailed documentation
│   ├── architecture.md
│   ├── reasoning.md
│   └── scaling_strategy.md
│
├── notebooks/            # Experimental or debugging notebooks
├── main.py               # Unified application launcher
├── requirements.txt      # Project dependencies
├── README.md             # This file
└── .env                  # Environment variables (API keys, etc.)
```

---

## 🚀 Quickstart Guide

Follow these steps to get the travel assistant running locally.

### 1. Setup Environment
Create and activate a Python virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Secrets
Create a `.env` file in the project root and add your API keys and database credentials.
```ini
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=your-pinecone-key
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=yourpassword
PINECONE_INDEX_NAME=vietnam-travel
PINECONE_VECTOR_DIM=1536
```

### 3. Load Data
Run the ingestion scripts to populate your databases.
```bash
# Load structured data into Neo4j
python -m scripts.load_to_neo4j

# Generate and upload embeddings to Pinecone
python -m scripts.upload_to_pinecone
```

### 4. Run the Application
Start the interactive command-line interface to chat with the assistant.
```bash
python -m scripts.chat_cli
```
*(Optional)* To view the graph visualization dashboard:
```bash
streamlit run scripts/dashboard.py
```

---

## 💡 Design Rationale: Why Hybrid Retrieval?

Combining a vector database with a graph database provides complementary strengths that a single system cannot offer.

* **Pinecone (Vector DB)** excels at semantic similarity search. It's perfect for understanding fuzzy or conceptual queries and finding relevant descriptive text (e.g., "find a place with a peaceful vibe").
* **Neo4j (Graph DB)** excels at reasoning over structured relationships. It's ideal for tasks requiring explicit connections, such as route planning, finding attractions within a city, or multi-hop queries (e.g., "find a hotel near a museum that serves vegan food").

The **hybrid benefit** is that semantic matches from Pinecone provide rich, relevant context, while the graph from Neo4j supplies logical constraints and connectivity. This grounds the LLM's reasoning, preventing it from recommending geographically impossible trips and improving the overall accuracy and explainability of its plans.

---

## ⚙️ Scaling, Reliability, and Maintenance

### Scaling Strategy (to 1M+ nodes)
* **Neo4j:** Utilize Neo4j Enterprise with causal clustering for horizontal scaling. Partition the graph logically (e.g., by region) and use read replicas to distribute query load. Ensure key properties are indexed and avoid returning full node data in high-traffic queries.
* **Pinecone:** Use sharded indexes or multiple namespaces. Optimize memory usage by tuning vector dimensions and using quantization techniques (e.g., IVF/PQ).
* **Orchestration:** Implement a caching layer (e.g., Redis) for hot queries. Deploy the application as independent microservices (e.g., using FastAPI) that can be autoscaled based on demand.

### Failure Modes & Mitigation
* **Data Inconsistency:** Use ingestion checkpoints and versioning to ensure the graph and vector databases are in sync.
* **Database Downtime:** The system is designed to gracefully fall back to a single-source retrieval mode (e.g., Pinecone-only) if one database is unavailable.
* **Token Limit / Prompt Size:** Context is trimmed and prioritized based on similarity scores to avoid exceeding LLM token limits.
* **Model Hallucination:** Responses are grounded by citing the specific node IDs and data retrieved from the databases. The model is prompted to state "I don't know" when confidence is low.
* **API Errors:** The LLM client implements automatic retries with exponential backoff and can use circuit-breaker patterns to handle rate limits or temporary API failures.

---

## 🔧 Future-Proofing and Extensibility

The architecture is designed to adapt to future changes in external APIs and to be easily extensible.

* **API Encapsulation:** All interactions with Pinecone and OpenAI are isolated within dedicated adapter modules (`pinecone_retriever.py`, `llm_client.py`). If an API changes, updates only need to be made in one place.
* **Compatibility Layers:** A thin compatibility layer can be introduced to manage multiple API versions simultaneously, controlled via environment variables.
* **Abstracted Interfaces:** By defining a generic `VectorStore` interface, the system can easily support other vector backends like Milvus, FAISS, or Weaviate with minimal code changes to the core orchestration logic.