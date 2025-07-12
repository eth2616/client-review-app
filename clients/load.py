import json

def load_clients_from_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ Failed to load client data: {e}")
        return []
