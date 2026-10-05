import argparse
from app.services.rag_engine import ConversationRAG


def main():
    parser = argparse.ArgumentParser(description="Search Inbox AI conversations.")
    parser.add_argument("query")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    engine = ConversationRAG()
    results = engine.search(args.query, args.top_k)

    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} | score={result['score']} ---")
        print(result["text"])


if __name__ == "__main__":
    main()
