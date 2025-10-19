import os
from dotenv import load_dotenv

# This line loads the variables from your .env file into the environment
load_dotenv()

# Now, read the variables from the environment
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# For variables that are numbers, you might need to convert them
PINECONE_VECTOR_DIM = int(os.getenv("PINECONE_VECTOR_DIM", 1536)) # default value
TOP_K = int(os.getenv("TOP_K", 5)) # default value