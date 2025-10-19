from app.hybrid.hybrid_chat import HybridChat

print("\n=== HybridChat System Test ===")
chat = HybridChat()

query = "Plan a 4-day cultural trip in Vietnam"
result = chat.handle_query(query)

print("\n=== Assistant Answer ===\n")
print(result["answer"])

print("\n=== Summary ===")
print(f"{len(result['matches'])} semantic matches, {len(result['graph_facts'])} graph facts.")
chat.close()
