from clients.classify import classify_client
from clients.summarize import summarize_client, get_client_json, summarize_client_json
from ai.openai_summary import generate_ai_summary
from utils.file_io import read_json, write_json
import json

# Load clients using refactored util
clients = read_json("clients.json")

# Classify clients
classified = [classify_client(c) for c in clients]

# Print debugging info
for client, result in zip(clients, classified):
    print(f"\n--- Debug: {client['name']} ---")
    print(summarize_client(client))
    print("\nFull JSON:")
    print(get_client_json(client))
    print("\nSummary JSON:")
    print(summarize_client_json(client))
    print("\nClassification Result:")
    print(json.dumps(result, indent=2))

# Save results
write_json(classified, "classified_clients.json")

# Generate summaries
print("\n🤖 AI Summaries for High-Risk Clients")
print("-" * 40)

for client, result in zip(clients, classified):
    if result["review_required"]:
        print(f"\n🔍 Summary for {client['name']}:")
        print(generate_ai_summary(client))
