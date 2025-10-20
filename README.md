# 🌴 Hybrid Travel Assistant

An **AI-powered travel planning system** that combines **semantic search (Pinecone)**, **graph-based reasoning (Neo4j)**, and **LLM reasoning (OpenAI GPT)** to deliver context-aware, connected, and personalized travel recommendations.

It also includes a **Streamlit interface** for interactive exploration and visualization of travel insights.

---

## 🚀 Features

✅ Semantic retrieval using **Pinecone**  
✅ Graph reasoning via **Neo4j** relationships  
✅ Contextual prompt building for **OpenAI ChatGPT**  
✅ In-memory caching for faster responses  
✅ Async pipeline for performance and concurrency  
✅ Rich **Streamlit UI** with live **knowledge graph visualization**  
✅ CLI support for debugging and testing  

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

```
            ┌────────────────────────────┐
            │        Streamlit UI        │
            │(User Query + Visualization)│
            └──────────────┬─────────────┘
                           │
                   [User enters query]
                           │
            ┌──────────────▼─────────────┐
            │       HybridChat           │
            │  (Async Orchestrator)      │
            └──────────────┬─────────────┘
                           │
   ┌───────────────────────┼─────────────────────────┐
   │                       │                         │
┌──▼───────────┐     ┌─────▼─────┐        ┌──────────▼───────┐
│ Pinecone     │     │  Neo4j    │        │  PromptBuilder   │
│ Retriever    │     │ Retriever │        │  + LLM Client    │
│ (Embeddings  │     │ (Graph    │        │  (OpenAI ChatGPT)│
│ + Similarity)│     │ Context)  │        └──────────────────┘
└──────────────┘     └───────────┘
                            │
                    ┌───────▼─────────┐
                    │ Structured Reply│
                    │ (Reasoned Output│
                    │  + Graph Facts) │
                    └─────────────────┘
                            │
                    [Returned to UI]
```
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
│
├── main.py               # Unified application launcher
├── requirements.txt      # Project dependencies
├── README.md             # This file
└── .env                  # Environment variables (API keys, etc.)
```
---

## ⚙️ Workflow

1. **User Query:** The traveler enters a request (e.g., “Romantic 4-day itinerary in Vietnam”).  
2. **Semantic Retrieval:** Pinecone retrieves top related nodes based on embeddings.  
3. **Graph Retrieval:** Neo4j fetches connected destinations, attractions, and relationships.  
4. **Prompt Assembly:** `PromptBuilder` combines semantic + graph context into a structured LLM prompt.  
5. **Reasoning:** OpenAI GPT model generates a rich, personalized plan.  
6. **Response Display:** The Streamlit UI shows the itinerary, summary, and live interactive graph.

---

## 🖥️ Streamlit Interface

### ✨ Chat UI Screenshot

![Streamlit Travel Assistant UI](outputs/image.png)

![Streamlit Travel Assistant UI](outputs/image2.png)

![Streamlit Travel Assistant UI](outputs/image3.png)

*(Example: Romantic 4-day itinerary in Vietnam — full reasoning and graph visualization.)*

---

## 🧩 Example CLI Usage

```bash
python -m scripts.chat_cli --query "Create a 4-day romantic trip to Vietnam"
```

## 🧩 Example UI Usage

```bash
python -m scripts.chat_cli --query "Create a 4-day romantic trip to Vietnam"
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
python -m streamlit run scripts/dashboard.py # (if error) run streamlit run scripts/dashboard.py
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


# 🌴 Hybrid AI Travel Assistant

> An intelligent travel planning system combining semantic search, knowledge graphs, and LLM reasoning to deliver personalized travel recommendations.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

---

## 📖 Overview

The Hybrid AI Travel Assistant leverages the complementary strengths of multiple AI technologies:

- **Pinecone**: Semantic vector search for understanding travel intent
- **Neo4j**: Graph database for structured relationship queries  
- **OpenAI GPT**: Natural language understanding and itinerary generation
- **Streamlit**: Interactive visualization and exploration interface

This hybrid approach grounds LLM responses with structured data while maintaining semantic understanding of user queries.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Hybrid Retrieval** | Combines vector similarity search with graph traversal for accurate, contextual results |
| 🧠 **Intelligent Reasoning** | Uses GPT models to synthesize information and generate personalized itineraries |
| ⚡ **Async Architecture** | Non-blocking I/O with `asyncio` for high-performance concurrent operations |
| 💾 **Smart Caching** | In-memory caching reduces API calls and improves response times |
| 🛡️ **Robust Error Handling** | Graceful fallbacks, custom exceptions, and automatic retry mechanisms |
| 📊 **Interactive Visualization** | Streamlit dashboard with live knowledge graph exploration |
| 🔧 **Developer Tools** | CLI interface, data loading scripts, and comprehensive logging |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
│         (User Query + Graph Visualization)              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  HybridChat Orchestrator                │
│              (Async Pipeline Coordinator)               │
└───┬──────────────────┬──────────────────┬───────────────┘
    │                  │                  │
    ▼                  ▼                  ▼
┌─────────┐      ┌──────────┐      ┌────────────────┐
│Pinecone │      │  Neo4j   │      │ PromptBuilder  │
│Vector DB│      │Graph DB  │      │   + OpenAI     │
└─────────┘      └──────────┘      └────────────────┘
    │                  │                  │
    └──────────────────┴──────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  AI Response   │
              │ (Grounded Plan)│
              └────────────────┘
```

### Design Principles

- **Separation of Concerns**: Retrievers, LLM client, and orchestration logic are fully decoupled
- **Modularity**: Each component can be tested, updated, or replaced independently
- **Extensibility**: Abstract interfaces allow swapping backends (e.g., Weaviate instead of Pinecone)

---

## 📁 Project Structure

```
hybrid_ai_travel_assistant/
├── app/
│   ├── retrievers/
│   │   ├── pinecone_retriever.py    # Semantic search
│   │   └── neo4j_retriever.py       # Graph queries
│   ├── llm/
│   │   ├── llm_client.py            # OpenAI wrapper
│   │   └── prompt_builder.py        # Context assembly
│   ├── hybrid/
│   │   ├── hybrid_retriever.py      # Retrieval orchestration
│   │   └── hybrid_chat.py           # Main reasoning engine
│   ├── config_loader.py             # Environment config
│   ├── exceptions.py                # Custom error types
│   └── logger.py                    # Logging setup
│
├── scripts/
│   ├── load_to_neo4j.py            # Data ingestion
│   ├── upload_to_pinecone.py       # Vector indexing
│   ├── visualize_graph.py          # Graph visualization
│   └── chat_cli.py                 # Interactive CLI
│
├── data/
│   └── vietnam_travel_dataset.json
│
├── tests/                          # Unit tests
├── logs/                           # Application logs
├── requirements.txt
├── .env.example                    # Environment template
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Neo4j (local or cloud instance)
- API keys for OpenAI and Pinecone

### 1. Clone & Setup Environment

```bash
# Clone repository
git clone https://github.com/yourusername/hybrid-travel-assistant.git
cd hybrid-travel-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```ini
# OpenAI
OPENAI_API_KEY=sk-...

# Pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=vietnam-travel
PINECONE_VECTOR_DIM=1536

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Optional
TOP_K=5
LOG_LEVEL=INFO
```

### 3. Load Data

```bash
# Load graph data into Neo4j
python -m scripts.load_to_neo4j

# Generate embeddings and upload to Pinecone
python -m scripts.upload_to_pinecone

# (Optional) Visualize the knowledge graph
python -m scripts.visualize_graph
```

### 4. Run the Application

**Interactive CLI:**
```bash
python -m scripts.chat_cli
```

**Streamlit CLI:**
```bash
python -m streamlit run scripts/chat_ui.py
```

---

## 💻 Usage Examples

### Command-Line Interface

```bash
$ python -m scripts.chat_cli

🌴 Hybrid Travel Assistant
Type your travel question (or 'exit' to quit):

> Create a romantic 4-day itinerary for Vietnam

🔍 Retrieving semantic matches...
🔗 Fetching graph context...
🤖 Generating personalized itinerary...

Here's your romantic 4-day Vietnam itinerary:
...
```

### Python API

```python
from app.hybrid.hybrid_chat import HybridChat

chat = HybridChat()
result = chat.handle_query("Best beaches in Vietnam for diving")

print(result["answer"])
print(f"Found {len(result['matches'])} semantic matches")
print(f"Retrieved {len(result['graph_facts'])} graph facts")

chat.close()
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Test specific component
python -m tests.test_hybrid_chat

# Test Pinecone connection
python -m tests.test_pinecone_retriever
```

---

## 💡 Design Rationale

### Why Hybrid Retrieval?

| Approach | Strengths | Use Case |
|----------|-----------|----------|
| **Vector Search (Pinecone)** | Semantic understanding, fuzzy matching | "Find peaceful destinations" |
| **Graph DB (Neo4j)** | Structured relationships, multi-hop queries | "Hotels near museums with vegan restaurants" |
| **Hybrid** | Best of both worlds + grounded reasoning | Complex, contextual travel planning |

**Key Benefits:**
- ✅ Semantic search finds relevant concepts
- ✅ Graph queries enforce logical constraints
- ✅ Combined context prevents hallucination
- ✅ Improved accuracy and explainability

---

## 📈 Scaling to 1M+ Nodes

### Database Optimization

**Neo4j:**
- Use Enterprise Edition with causal clustering
- Implement read replicas for query distribution
- Partition data by region/type
- Index frequently queried properties
- Limit result set sizes

**Pinecone:**
- Use namespaces for logical separation
- Implement vector quantization (IVF/PQ)
- Consider sharding for very large datasets
- Cache hot queries in Redis

### Application Architecture

```
┌─────────────┐
│ Load Bal.   │
└──────┬──────┘
       │
   ┌───┴───┬────────┬────────┐
   ▼       ▼        ▼        ▼
┌─────┐ ┌─────┐  ┌─────┐  ┌─────┐
│API 1│ │API 2│  │API 3│  │API 4│
└──┬──┘ └──┬──┘  └──┬──┘  └──┬──┘
   │       │        │        │
   └───────┴────────┴────────┘
                │
          ┌─────┴─────┐
          ▼           ▼
        ┌────────┐  ┌────────┐
        │ Redis  │  │Pinecone│
        │ Cache  │  │ Neo4j  │
        └────────┘  └────────┘
```

**Strategies:**
- Deploy as microservices (FastAPI)
- Implement Redis caching layer
- Use connection pooling
- Enable horizontal autoscaling
- Monitor with Prometheus/Grafana

---

## 🛡️ Error Handling & Reliability

### Failure Modes

| Issue | Mitigation |
|-------|------------|
| Database downtime | Graceful degradation (single-source mode) |
| API rate limits | Exponential backoff with jitter |
| Token limit exceeded | Context trimming and prioritization |
| Data inconsistency | Versioning and checkpointing |
| Model hallucination | Citation of sources, confidence scoring |

### Circuit Breaker Pattern

```python
# Automatic fallback if Neo4j is unavailable
try:
    graph_facts = neo4j_retriever.fetch_context(node_ids)
except GraphError:
    logger.warning("Neo4j unavailable, falling back to semantic-only")
    graph_facts = []
```

---

## 🔮 Future Enhancements

- [ ] Multi-language support (embedding models)
- [ ] User preference learning (collaborative filtering)
- [ ] Real-time price integration
- [ ] Mobile app (React Native)
- [ ] Voice interface (Whisper API)
- [ ] A/B testing framework for prompt optimization
- [ ] GraphRAG for advanced reasoning
- [ ] Integration with booking APIs

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT models and embeddings
- Pinecone for vector database infrastructure
- Neo4j for graph database technology
- The Python community for excellent libraries

---

## 📧 Contact

For questions or feedback, please open an issue or contact:
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

---

<div align="center">
  <strong>Built with ❤️ for intelligent travel planning</strong>
</div>