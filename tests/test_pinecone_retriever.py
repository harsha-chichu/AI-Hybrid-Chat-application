from app.retrievers.pinecone_retriever import PineconeRetriever

# """To Check the index name is present in Pinecone."""
# r = PineconeRetriever()
# print("Available indexes:", r.pc.list_indexes().names())


if __name__ == "__main__":
    retriever = PineconeRetriever()
    results = retriever.query("romantic destinations in Vietnam") or []
    if not results:
        print("No results found - maybe the index is empty.")
    else:
        print(f"Top match IDs: {[m['id'] for m in results]}")


