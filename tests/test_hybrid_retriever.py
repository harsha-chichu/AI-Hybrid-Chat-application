from app.hybrid.hybrid_retriever import HybridRetriever

if __name__ == "__main__":
    retriever = HybridRetriever()
    query = "Suggest a cultural 3-day itinerary in Hanoi"
    result = retriever.retrieve(query)

    print("\n=== Hybrid Retrieval Test ===")
    print(result["summary"])
    print("Top semantic match IDs:", [m["id"] for m in result["semantic_matches"][:5]])
    print("Sample graph fact:", result["graph_facts"][:2])
