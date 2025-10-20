#test 1

# from app.hybrid.hybrid_chat import HybridChat

# print("\n=== HybridChat System Test ===")
# chat = HybridChat()

# query = "Plan a 4-day cultural trip in Vietnam"
# result = chat.handle_query(query)

# print("\n=== Assistant Answer ===\n")
# print(result["answer"])

# print("\n=== Summary ===")
# print(f"{len(result['matches'])} semantic matches, {len(result['graph_facts'])} graph facts.")
# chat.close()

#-----------------------------------

# test 2

# from app.hybrid.hybrid_chat import HybridChat

# chat = HybridChat(enable_cache=True)
# query = "Create a romantic 4-day itinerary for Vietnam"

# # First call – should MISS cache
# result1 = chat.handle_query(query)
# print("\n--- FIRST RUN ---")
# print("Cached:", result1["cached"])
# print("Answer snippet:", result1["answer"][:300])

# # Second call – should HIT cache
# result2 = chat.handle_query(query)
# print("\n--- SECOND RUN ---")
# print("Cached:", result2["cached"])

# # Check cache stats
# print("\nCache Stats:", chat.get_cache_stats())
# chat.close()

#-----------------------------------

# test 3

# scripts/simple_test.py
import asyncio
from app.hybrid.hybrid_chat import HybridChat

# This is an async function because our chat logic is async
async def run_tests():
    """
    A simple script to test caching and live responses from HybridChat.
    """
    print("--- Initializing Hybrid Chat ---")
    chat = HybridChat(enable_cache=True)
    query = "Suggest a 3-day itinerary in Hanoi"

    try:
        # --- Test 1: Caching ---
        print("\n--- Testing Caching Logic ---")
        
        # First call – should be a CACHE MISS
        print("Running first query (expecting a cache MISS)...")
        result1 = await chat.handle_query_async(query)
        print(f"Cached: {result1['cached']}")
        print(f"Answer snippet: {result1['answer'][:100]}...")
        
        # A simple check to confirm it wasn't cached
        assert not result1['cached'], "FAIL: First run should not be cached!"
        
        # Second call – should be a CACHE HIT
        print("\nRunning second query (expecting a cache HIT)...")
        result2 = await chat.handle_query_async(query)
        print(f"Cached: {result2['cached']}")
        
        # A simple check to confirm it WAS cached
        assert result2['cached'], "FAIL: Second run should have been cached!"
        
        print("\nCaching test passed successfully!")

    except Exception as e:
        print(f"\n--- An error occurred: {e} ---")
    finally:
        # This part always runs to make sure connections are closed
        print("\n--- Closing connections ---")
        chat.close()

# Use asyncio.run() to execute our async function
if __name__ == "__main__":
    asyncio.run(run_tests())
