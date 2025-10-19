from app.retrievers.neo4j_retriever import Neo4jRetriever

if __name__ == "__main__":
    retriever = Neo4jRetriever()
    facts = retriever.fetch_neighbors(["city_hanoi", "city_hue"])
    print(f"Retrieved {len(facts)} relationships.")
    if facts:
        print(facts[:3])
    retriever.close()
