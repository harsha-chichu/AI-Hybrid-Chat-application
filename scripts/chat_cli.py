"""
Interactive CLI for the Hybrid Travel Assistant.

Usage:
  python -m scripts.chat_cli                -> interactive prompt
  python -m scripts.chat_cli --query "..."  -> single query
  python -m scripts.chat_cli --no-cache     -> disable caching
"""

import argparse
from app.hybrid.hybrid_chat import HybridChat
from app.logger import get_logger
from rich.console import Console
from rich.markdown import Markdown

logger = get_logger(__name__)

console = Console()


def run_interactive(chat: HybridChat):
    print("Hybrid Travel Assistant (type 'exit' or Ctrl+C to quit)\n")
    try:
        while True:
            q = input("Enter your travel question: ").strip()
            if not q or q.lower() in ("exit", "quit"):
                break
            print("\nThinking...\n")
            result = chat.handle_query(q)
            print_result(result)
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        chat.close()


def print_result(result: dict):
    """Render model output nicely using rich markdown."""
    answer = result.get("answer", "")
    matches = result.get("matches", [])
    facts = result.get("graph_facts", [])
    cached = result.get("cached", False)
    ts = result.get("timestamp", "")

    hdr = f"[bold cyan]{'[Cached]' if cached else '[Fresh]'}[/bold cyan]"
    console.print(f"\n{hdr} [dim]Response generated at {ts}[/dim]\n")

    # --- Print model's main answer ---
    if answer:
        console.print(Markdown(answer))
    else:
        console.print("[red]No answer returned from model.[/red]")

    # --- Add summary section ---
    from app.hybrid.hybrid_retriever import HybridRetriever  # lightweight import here
    retriever = HybridRetriever()
    summary = retriever.search_summary(result)
    console.print("\n[bold yellow]Quick Summary:[/bold yellow]")
    console.print(Markdown(summary))
    console.print()  # spacing

    # --- Print metadata ---
    console.rule("[dim]Metadata[/dim]")
    console.print(f"[green]Semantic matches:[/green] {len(matches)}")
    console.print(f"[green]Graph facts:[/green] {len(facts)}")

    top_ids = [m.get("id") for m in matches[:5]]
    if top_ids:
        console.print(f"[cyan]Top match IDs:[/cyan] {', '.join(top_ids)}")

    console.print()




def run_single_query(chat: HybridChat, query: str):
    print("Running single query...\n")
    result = chat.handle_query(query)
    print_result(result)
    chat.close()


def main():
    parser = argparse.ArgumentParser(description="Hybrid Travel Assistant CLI")
    parser.add_argument("--query", type=str, help="Run a single query and exit")
    parser.add_argument("--no-cache", action="store_true", help="Disable retrieval cache")
    args = parser.parse_args()

    chat = HybridChat(enable_cache=not args.no_cache)

    if args.query:
        run_single_query(chat, args.query)
        return

    run_interactive(chat)


if __name__ == "__main__":
    main()
