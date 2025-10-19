hybrid_ai_travel_assistant/
│
├── app/                                      # Core application logic
│   ├── __init__.py
│   ├── config_loader.py                      # Loads environment variables (.env)
│   ├── logger.py                             # Centralized logging setup
│   ├── exceptions.py                         # Custom exception classes
│   │
│   ├── retrievers/                           # Retrieval modules
│   │   ├── __init__.py
│   │   ├── pinecone_retriever.py             # Pinecone: embedding + semantic vector search
│   │   └── neo4j_retriever.py                # Neo4j: graph traversal + context fetching
│   │
│   ├── llm/                                  # LLM interaction layer
│   │   ├── __init__.py
│   │   ├── llm_client.py                     # OpenAI wrapper (embeddings + chat)
│   │   └── prompt_builder.py                 # Builds structured prompts for LLM
│   │
│   ├── hybrid/                               # Combines retrievers + LLM logic
│   │   ├── __init__.py
│   │   ├── hybrid_retriever.py               # Orchestrates vector + graph retrieval
│   │   └── hybrid_chat.py                    # Main reasoning + response orchestration
│   │
│   └── utils/                                # Misc. helpers
│       ├── __init__.py
│       ├── timer.py                          # Measure retrieval/response time
│       └── text_cleaner.py                   # (optional) preprocess text before embedding
│
├── scripts/                                  # Command-line tools for developers
│   ├── load_to_neo4j.py                      # Load dataset into Neo4j
│   ├── upload_to_pinecone.py                 # Upload embeddings to Pinecone
│   ├── visualize_graph.py                    # Create PyVis visualization
│   └── chat_cli.py                           # Interactive hybrid chat CLI
│
├── data/                                     # Data assets
│   ├── vietnam_travel_dataset.json
│   └── samples/                              # Additional or test datasets
│
├── config/                                   # Configuration constants
│   ├── __init__.py
│   └── config.py                             # Reads env vars via dotenv or os.getenv
│
├── tests/                                    # Unit & integration tests
│   ├── __init__.py
│   ├── test_pinecone_retriever.py
│   ├── test_neo4j_retriever.py
│   └── test_hybrid_chat.py
│
├── logs/                                     # Runtime logs
│   └── app.log
│
├── docs/                                     # Documentation for reviewers / teammates
│   ├── architecture.md                       # System design diagram + data flow
│   ├── reasoning.md                          # Why Neo4j + Pinecone hybrid
│   └── scaling_strategy.md                   # Scaling to 1 million nodes + fault tolerance
│
├── notebooks/                                # Optional experiments or debugging
│   ├── retrieval_tests.ipynb
│   └── response_quality.ipynb
│
├── main.py                                   # Unified launcher (e.g. calls HybridChat)
├── requirements.txt                          # Dependencies
├── README.md                                 # Setup + usage instructions
├── .env                                      # API keys (ignored in git)
└── setup.py                                  # Optional — enables pip install
