"""
PromptBuilder combines semantic and graph-based context
to form a structured message list for chat completion.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class PromptBuilder:
    """
    Builds LLM-ready prompts using retrieved text and graph context.
    """

    def __init__(self):
        logger.info("PromptBuilder initialized.")

    def build_prompt(self, query: str, matches: List[Dict], graph_facts: List[Dict]) -> List[Dict]:
        """
        Construct a structured chat prompt from user query, Pinecone matches, and Neo4j graph facts.
        Returns a list of messages suitable for OpenAI Chat API.
        """
        try:
            # Summarize retrieved text
            semantic_context = "\n".join(
                [f"- {m['metadata'].get('text', '')[:400]}" for m in matches if "metadata" in m]
            )

            # Summarize graph relationships
            graph_context = "\n".join(
                [f"- {f['source']} --({f['rel']})--> {f['target_name']}: {f['target_desc']}"
                 for f in graph_facts]
            )

            system_prompt = (
                "You are a knowledgeable assistant helping users explore Vietnam travel insights. "
                "Use the semantic and graph context to answer factually and coherently. "
                "Avoid speculation. If unsure, state that clearly."
            )

            user_prompt = (
                f"User question: {query}\n\n"
                f"Relevant text snippets:\n{semantic_context}\n\n"
                f"Graph relationships:\n{graph_context}\n\n"
                "Answer concisely, using factual and contextual details where possible."
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            logger.info("Prompt built successfully.")
            return messages

        except Exception as e:
            logger.exception("Failed to build prompt.")
            raise ValueError(f"Prompt building failed: {e}")
