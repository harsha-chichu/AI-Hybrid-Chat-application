from app.hybrid.hybrid_chat import HybridChat
chat = HybridChat()
res = chat.handle_query("Plan a 4 day romantic trip to Vietnam")
print(res['answer'][:500])
chat.close()
