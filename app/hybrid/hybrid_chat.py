# """
# HybridChat orchestrates retrieval from Pinecone and Neo4j,
# builds prompts, and queries OpenAI’s chat model for reasoning.
# """

# import logging
# from typing import List, Dict
# from app.retrievers.pinecone_retriever import PineconeRetriever
# from app.retrievers.neo4j_retriever import Neo4jRetriever
# from app.llm.llm_client import embed_text, chat_completion
# from app.llm.prompt_builder import PromptBuilder
# from app.exceptions import RetrievalError, LLMError

# logger = logging.getLogger(__name__)

# class HybridChat:
#     """
#     The reasoning orchestrator that merges vector + graph context
#     for intelligent conversational responses.
#     """

#     def __init__(self):
#         self.pinecone = PineconeRetriever()
#         self.neo4j = Neo4jRetriever()
#         self.prompt_builder = PromptBuilder()
#         logger.info("HybridChat initialized.")

#     def handle_query(self, query: str, top_k: int = 5) -> Dict:
#         """End-to-end reasoning pipeline."""
#         try:
#             logger.info(f"Handling user query: {query}")

#             # 1. Semantic retrieval
#             matches = self.pinecone.query(query, top_k=top_k)
#             match_ids = [m["id"] for m in matches]
#             logger.info(f"Retrieved {len(matches)} semantic matches.")

#             # 2. Graph context
#             graph_facts = self.neo4j.fetch_graph_context(match_ids)
#             logger.info(f"Retrieved {len(graph_facts)} graph facts.")

#             # 3. Prompt creation
#             messages = self.prompt_builder.build_prompt(query, matches, graph_facts)

#             # 4. LLM reasoning
#             answer = chat_completion(messages)

#             # 5. Final structured output
#             return {
#                 "query": query,
#                 "matches": matches,
#                 "graph_facts": graph_facts,
#                 "answer": answer,
#             }

#         except (RetrievalError, LLMError) as e:
#             logger.error(f"Known error: {e}")
#             raise
#         except Exception as e:
#             logger.exception("Hybrid reasoning failed.")
#             raise RetrievalError(f"Hybrid reasoning failed: {e}")

#     def close(self):
#         """Clean up resources."""
#         self.neo4j.close()


# """
# Enhanced HybridChat with async operations and caching for better performance.
# """

# import logging
# import asyncio
# import hashlib
# import json
# from typing import List, Dict, Optional
# from functools import lru_cache
# from datetime import datetime, timedelta

# from app.retrievers.pinecone_retriever import PineconeRetriever
# from app.retrievers.neo4j_retriever import Neo4jRetriever
# from app.llm.llm_client import chat_completion
# from app.llm.prompt_builder import PromptBuilder
# from app.exceptions import RetrievalError, LLMError

# logger = logging.getLogger(__name__)

# class SimpleCache:
#     """Simple in-memory cache with TTL."""
    
#     def __init__(self, ttl_seconds: int = 3600):
#         self.cache = {}
#         self.ttl_seconds = ttl_seconds
    
#     def get(self, key: str) -> Optional[any]:
#         """Get value from cache if not expired."""
#         if key in self.cache:
#             value, timestamp = self.cache[key]
#             if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
#                 logger.info(f"Cache HIT for key: {key[:50]}...")
#                 return value
#             else:
#                 del self.cache[key]
#         logger.info(f"Cache MISS for key: {key[:50]}...")
#         return None
    
#     def set(self, key: str, value: any):
#         """Set value in cache with timestamp."""
#         self.cache[key] = (value, datetime.now())
#         logger.debug(f"Cache SET for key: {key[:50]}...")
    
#     def clear(self):
#         """Clear all cache."""
#         self.cache.clear()
#         logger.info("Cache cleared.")

# class AsyncHybridChat:
#     """
#     Enhanced reasoning orchestrator with async operations and caching.
#     """

#     def __init__(self, enable_cache: bool = True):
#         self.pinecone = PineconeRetriever()
#         self.neo4j = Neo4jRetriever()
#         self.prompt_builder = PromptBuilder()
#         self.enable_cache = enable_cache
#         self.cache = SimpleCache(ttl_seconds=3600) if enable_cache else None
#         logger.info(f"AsyncHybridChat initialized (caching: {enable_cache}).")

#     def _generate_cache_key(self, query: str, top_k: int) -> str:
#         """Generate cache key from query and parameters."""
#         key_string = f"{query}:{top_k}"
#         return hashlib.md5(key_string.encode()).hexdigest()

#     async def _fetch_semantic_matches_async(self, query: str, top_k: int) -> List[Dict]:
#         """Async wrapper for Pinecone query."""
#         # Run blocking I/O in executor
#         loop = asyncio.get_event_loop()
#         matches = await loop.run_in_executor(
#             None, 
#             self.pinecone.query, 
#             query, 
#             top_k
#         )
#         return matches

#     async def _fetch_graph_context_async(self, node_ids: List[str]) -> List[Dict]:
#         """Async wrapper for Neo4j query."""
#         if not node_ids:
#             return []
#         loop = asyncio.get_event_loop()
#         graph_facts = await loop.run_in_executor(
#             None,
#             self.neo4j.fetch_graph_context,
#             node_ids
#         )
#         return graph_facts

#     async def handle_query_async(self, query: str, top_k: int = 5) -> Dict:
#         """Async end-to-end reasoning pipeline with parallel retrieval."""
#         try:
#             logger.info(f"[ASYNC] Handling user query: {query}")
            
#             # Check cache
#             if self.enable_cache:
#                 cache_key = self._generate_cache_key(query, top_k)
#                 cached_result = self.cache.get(cache_key)
#                 if cached_result:
#                     logger.info("Returning cached result")
#                     return cached_result

#             # 1. Start semantic retrieval
#             semantic_task = asyncio.create_task(
#                 self._fetch_semantic_matches_async(query, top_k)
#             )
            
#             # Wait for semantic results to get IDs
#             matches = await semantic_task
#             match_ids = [m["id"] for m in matches]
#             logger.info(f"[ASYNC] Retrieved {len(matches)} semantic matches.")

#             # 2. Start graph retrieval (now we have IDs)
#             graph_task = asyncio.create_task(
#                 self._fetch_graph_context_async(match_ids)
#             )
            
#             # 3. Wait for graph results
#             graph_facts = await graph_task
#             logger.info(f"[ASYNC] Retrieved {len(graph_facts)} graph facts.")

#             # 4. Prompt creation (sync, fast)
#             messages = self.prompt_builder.build_prompt(query, matches, graph_facts)

#             # 5. LLM reasoning (run in executor)
#             loop = asyncio.get_event_loop()
#             answer = await loop.run_in_executor(
#                 None,
#                 chat_completion,
#                 messages
#             )

#             # 6. Final structured output
#             result = {
#                 "query": query,
#                 "matches": matches,
#                 "graph_facts": graph_facts,
#                 "answer": answer,
#                 "cached": False,
#                 "timestamp": datetime.now().isoformat()
#             }
            
#             # Cache the result
#             if self.enable_cache:
#                 self.cache.set(cache_key, result)

#             return result

#         except (RetrievalError, LLMError) as e:
#             logger.error(f"Known error: {e}")
#             raise
#         except Exception as e:
#             logger.exception("[ASYNC] Hybrid reasoning failed.")
#             raise RetrievalError(f"Async hybrid reasoning failed: {e}")

#     def handle_query(self, query: str, top_k: int = 5) -> Dict:
#         """Synchronous wrapper for async query handling."""
#         try:
#             # Run async function in event loop
#             loop = asyncio.get_event_loop()
#             if loop.is_running():
#                 # If loop is already running, create new task
#                 return asyncio.create_task(self.handle_query_async(query, top_k))
#             else:
#                 # Run in new event loop
#                 return loop.run_until_complete(
#                     self.handle_query_async(query, top_k)
#                 )
#         except Exception as e:
#             logger.exception("Sync wrapper failed")
#             raise

#     def get_cache_stats(self) -> Dict:
#         """Get cache statistics."""
#         if not self.enable_cache:
#             return {"enabled": False}
#         return {
#             "enabled": True,
#             "size": len(self.cache.cache),
#             "ttl_seconds": self.cache.ttl_seconds
#         }

#     def clear_cache(self):
#         """Clear the cache."""
#         if self.enable_cache:
#             self.cache.clear()

#     def close(self):
#         """Clean up resources."""
#         self.neo4j.close()
#         if self.enable_cache:
#             self.cache.clear()
#         logger.info("AsyncHybridChat closed.")


# # Backward compatibility - keep original class name
# class HybridChat(AsyncHybridChat):
#     """Alias for AsyncHybridChat to maintain backward compatibility."""
#     pass

"""
Enhanced HybridChat with async operations, caching, retry, and graceful fallback.
"""

import logging
import asyncio
import hashlib
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from app.retrievers.pinecone_retriever import PineconeRetriever
from app.retrievers.neo4j_retriever import Neo4jRetriever
from app.llm.llm_client import chat_completion
from app.llm.prompt_builder import PromptBuilder
from app.exceptions import RetrievalError, LLMError

logger = logging.getLogger(__name__)


# ============================================================
# Thread-safe in-memory cache with TTL
# ============================================================
class SimpleCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, Any] = {}
        self.ttl_seconds = ttl_seconds
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            entry = self.cache.get(key)
            if not entry:
                logger.debug(f"[CACHE] MISS for {key[:12]}")
                return None
            value, timestamp = entry
            if datetime.now() - timestamp < timedelta(seconds=self.ttl_seconds):
                logger.debug(f"[CACHE] HIT for {key[:12]}")
                return value
            else:
                logger.debug(f"[CACHE] EXPIRED for {key[:12]}")
                del self.cache[key]
                return None

    def set(self, key: str, value: Any):
        with self.lock:
            self.cache[key] = (value, datetime.now())

    def clear(self):
        with self.lock:
            self.cache.clear()
        logger.info("[CACHE] Cleared all entries.")


# ============================================================
# Async Hybrid Chat
# ============================================================
class AsyncHybridChat:
    def __init__(self, enable_cache: bool = True):
        self.pinecone = PineconeRetriever()
        self.neo4j = Neo4jRetriever()
        self.prompt_builder = PromptBuilder()
        self.enable_cache = enable_cache
        self.cache = SimpleCache(ttl_seconds=3600) if enable_cache else None
        logger.info(f"AsyncHybridChat initialized (cache: {enable_cache}).")

    # --------------------- UTILITIES ---------------------
    def _generate_cache_key(self, query: str, top_k: int) -> str:
        return hashlib.md5(f"{query}:{top_k}".encode()).hexdigest()

    async def _retry_async(self, func, *args, retries=3, delay=2, **kwargs):
        """Retry wrapper for transient errors."""
        for attempt in range(1, retries + 1):
            try:
                return await asyncio.to_thread(func, *args, **kwargs)
            except Exception as e:
                logger.warning(f"[Retry {attempt}/{retries}] {func.__name__} failed: {e}")
                if attempt < retries:
                    await asyncio.sleep(delay)
        raise RetrievalError(f"{func.__name__} failed after {retries} retries")

    # --------------------- CORE PIPELINE ---------------------
    async def handle_query_async(self, query: str, top_k: int = 5) -> Dict:
        try:
            logger.info(f"[ASYNC] Handling user query: {query}")

            # Check cache
            cache_key = self._generate_cache_key(query, top_k)
            if self.enable_cache:
                cached = self.cache.get(cache_key)
                if cached:
                    cached["cached"] = True
                    logger.info(f"[CACHE] Returning cached result for query: {query[:30]}...")
                    return cached

            # Step 1 – Semantic search (async)
            matches = await self._retry_async(self.pinecone.query, query, top_k)
            match_ids = [m["id"] for m in matches]
            logger.info(f"[ASYNC] Retrieved {len(matches)} Pinecone matches.")

            # Step 2 – Graph context (parallel)
            graph_facts = []
            try:
                graph_facts = await self._retry_async(self.neo4j.fetch_graph_context, match_ids)
                logger.info(f"[ASYNC] Retrieved {len(graph_facts)} Neo4j facts.")
            except Exception as e:
                logger.warning(f"[FALLBACK] Neo4j retrieval failed — continuing with semantic data only: {e}")

            # Step 3 – Prompt creation
            messages = self.prompt_builder.build_prompt(query, matches, graph_facts)

            # Step 4 – LLM reasoning (retry-safe)
            answer = await self._retry_async(chat_completion, messages)

            # Step 5 – Structure output
            result = {
                "query": query,
                "matches": matches,
                "graph_facts": graph_facts,
                "answer": answer,
                "cached": False,
                "timestamp": datetime.now().isoformat()
            }

            if self.enable_cache:
                self.cache.set(cache_key, result)

            return result

        except (RetrievalError, LLMError) as e:
            logger.error(f"[ASYNC] Known error: {e}")
            raise
        except Exception as e:
            logger.exception("[ASYNC] Hybrid reasoning failed.")
            raise RetrievalError(f"Async hybrid reasoning failed: {e}")

    # --------------------- SYNC WRAPPER ---------------------
    def handle_query(self, query: str, top_k: int = 5) -> Dict:
        """Safe synchronous wrapper for Streamlit or CLI use."""
        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # Streamlit thread has no default loop - create one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                # Running inside another async loop
                future = asyncio.ensure_future(self.handle_query_async(query, top_k))
                return loop.run_until_complete(future)
            else:
                return loop.run_until_complete(self.handle_query_async(query, top_k))
        except Exception as e:
            logger.exception("Error during handle_query execution")
            raise RetrievalError(f"Error executing hybrid query: {e}")


    # --------------------- MAINTENANCE ---------------------
    def get_cache_stats(self) -> Dict:
        if not self.enable_cache:
            return {"enabled": False}
        return {
            "enabled": True,
            "size": len(self.cache.cache),
            "ttl_seconds": self.cache.ttl_seconds
        }

    def clear_cache(self):
        if self.enable_cache:
            self.cache.clear()

    def close(self):
        self.neo4j.close()
        if self.enable_cache:
            self.cache.clear()
        logger.info("AsyncHybridChat closed.")


# ============================================================
# Backward-compatible alias
# ============================================================
class HybridChat(AsyncHybridChat):
    """Alias for AsyncHybridChat (kept for backward compatibility)."""
    pass
