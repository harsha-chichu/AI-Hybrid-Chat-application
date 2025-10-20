from app.llm.llm_client import embed_text, chat_completion

if __name__ == "__main__":
    print("Testing embedding generation...")
    emb = embed_text("Vietnam travel itinerary")
    print(f"✅ Embedding length: {len(emb)}")

    print("\nTesting chat completion...")
    msg = [
        {"role": "system", "content": "You are a travel assistant."},
        {"role": "user", "content": "Suggest a 2-day itinerary for Hanoi."}
    ]
    resp = chat_completion(msg)
    print("\n✅ Chat response:")
    print(resp)
