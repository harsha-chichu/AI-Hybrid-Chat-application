# """
# PromptBuilder combines semantic and graph-based context
# to form a structured message list for chat completion.
# """

# import logging
# from typing import List, Dict

# logger = logging.getLogger(__name__)

# class PromptBuilder:
#     """
#     Builds LLM-ready prompts using retrieved text and graph context.
#     """

#     def __init__(self):
#         logger.info("PromptBuilder initialized.")

#     def build_prompt(self, query: str, matches: List[Dict], graph_facts: List[Dict]) -> List[Dict]:
#         """
#         Construct a structured chat prompt from user query, Pinecone matches, and Neo4j graph facts.
#         Returns a list of messages suitable for OpenAI Chat API.
#         """
#         try:
#             # Summarize retrieved text
#             semantic_context = "\n".join(
#                 [f"- {m['metadata'].get('text', '')[:400]}" for m in matches if "metadata" in m]
#             )

#             # Summarize graph relationships
#             graph_context = "\n".join(
#                 [f"- {f['source']} --({f['rel']})--> {f['target_name']}: {f['target_desc']}"
#                  for f in graph_facts]
#             )

#             system_prompt = (
#                 "You are a knowledgeable assistant helping users explore Vietnam travel insights. "
#                 "Use the semantic and graph context to answer factually and coherently. "
#                 "Avoid speculation. If unsure, state that clearly."
#             )

#             user_prompt = (
#                 f"User question: {query}\n\n"
#                 f"Relevant text snippets:\n{semantic_context}\n\n"
#                 f"Graph relationships:\n{graph_context}\n\n"
#                 "Answer concisely, using factual and contextual details where possible."
#             )

#             messages = [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt},
#             ]

#             logger.info("Prompt built successfully.")
#             return messages

#         except Exception as e:
#             logger.exception("Failed to build prompt.")
#             raise ValueError(f"Prompt building failed: {e}")

"""
Enhanced PromptBuilder with advanced reasoning and context structuring.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class PromptBuilder:
    """
    Builds LLM-ready prompts using retrieved text and graph context.
    Enhanced with chain-of-thought reasoning and structured context.
    """

    def __init__(self):
        logger.info("Enhanced PromptBuilder initialized.")

    def build_prompt(self, query: str, matches: List[Dict], graph_facts: List[Dict]) -> List[Dict]:
        """
        Construct an enhanced structured chat prompt with better context organization.
        Returns a list of messages suitable for OpenAI Chat API.
        """
        try:
            # Organize semantic context by type
            context_by_type = self._organize_by_type(matches)
            
            # Build structured semantic context
            semantic_context = self._build_semantic_context(context_by_type)
            
            # Build enhanced graph context with relationship insights
            graph_context = self._build_graph_context(graph_facts)
            
            # Enhanced system prompt with reasoning instructions
            system_prompt = self._build_system_prompt()
            
            # Enhanced user prompt with structured thinking
            user_prompt = self._build_user_prompt(query, semantic_context, graph_context)

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            logger.info("Enhanced prompt built successfully.")
            return messages

        except Exception as e:
            logger.exception("Failed to build enhanced prompt.")
            raise ValueError(f"Prompt building failed: {e}")

    def _organize_by_type(self, matches: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize matches by entity type (City, Attraction, Hotel, Activity)."""
        organized = {}
        for match in matches:
            if "metadata" not in match:
                continue
            entity_type = match["metadata"].get("type", "Unknown")
            if entity_type not in organized:
                organized[entity_type] = []
            organized[entity_type].append(match)
        return organized

    def _build_semantic_context(self, context_by_type: Dict[str, List[Dict]]) -> str:
        """Build structured semantic context organized by entity type."""
        sections = []
        
        for entity_type, items in context_by_type.items():
            if not items:
                continue
                
            section = [f"\n**{entity_type}s:**"]
            for item in items[:5]:  # Limit to top 5 per type
                metadata = item.get("metadata", {})
                name = metadata.get("name", "Unknown")
                city = metadata.get("city", "")
                tags = metadata.get("tags", [])
                
                # Build rich description
                desc_parts = [f"• {name}"]
                if city:
                    desc_parts.append(f"(in {city})")
                if tags:
                    desc_parts.append(f"- Tags: {', '.join(tags[:3])}")
                
                section.append(" ".join(desc_parts))
            
            sections.append("\n".join(section))
        
        return "\n".join(sections) if sections else "No specific semantic matches found."

    def _build_graph_context(self, graph_facts: List[Dict]) -> str:
        """Build enhanced graph context showing relationships and connections."""
        if not graph_facts:
            return "No graph relationships found."
        
        # Group by source
        relationships_by_source = {}
        for fact in graph_facts:
            source = fact.get("source", "Unknown")
            if source not in relationships_by_source:
                relationships_by_source[source] = []
            relationships_by_source[source].append(fact)
        
        sections = []
        sections.append("**Connected Destinations & Features:**")
        
        for source, facts in list(relationships_by_source.items())[:5]:  # Top 5 sources
            rel_list = []
            for fact in facts[:3]:  # Top 3 relationships per source
                rel_type = fact.get("rel", "related_to")
                target = fact.get("target_name", "Unknown")
                rel_list.append(f"{target} ({rel_type})")
            
            if rel_list:
                sections.append(f"• {source}: {', '.join(rel_list)}")
        
        return "\n".join(sections)

    def _build_system_prompt(self) -> str:
        """Build enhanced system prompt with reasoning instructions."""
        return """You are an expert Vietnam travel advisor with deep knowledge of Vietnamese culture, destinations, and travel planning.

Your expertise includes:
- Crafting personalized itineraries based on traveler preferences
- Understanding seasonal variations and best travel times
- Knowledge of authentic local experiences and hidden gems
- Practical travel logistics (transport, accommodation, dining)
- Cultural sensitivity and local customs

When answering queries:
1. **Analyze** the user's preferences and constraints
2. **Consider** both semantic matches (destinations/activities) and graph relationships (connected places)
3. **Reason** about logical travel routes and timing
4. **Provide** specific, actionable recommendations
5. **Explain** why each recommendation fits the user's needs
6. **Be honest** if information is limited or uncertain

Response style:
- Be warm, enthusiastic, and encouraging
- Structure complex answers with clear sections
- Include practical details (duration, best times, tips)
- Mention connections between destinations when relevant
- Always cite the context provided in your response"""

    def _build_user_prompt(self, query: str, semantic_context: str, graph_context: str) -> str:
        """Build enhanced user prompt with structured thinking."""
        return f"""**Travel Query:** {query}

**Available Context:**

{semantic_context}

{graph_context}

**Instructions:**
Please create a comprehensive response that:
1. Addresses the specific request in the query
2. Uses the provided destinations, attractions, hotels, and activities
3. Considers the geographical connections shown in the graph
4. Provides a day-by-day breakdown if it's an itinerary request
5. Includes practical travel tips and recommendations
6. Explains your reasoning for each suggestion

Think through this step-by-step and provide a well-structured, helpful response."""
