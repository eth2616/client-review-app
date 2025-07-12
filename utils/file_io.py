import json

def read_json(file_path):
    """Reads a JSON file and returns the parsed data."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return []

def write_json(data, file_path):
    """Writes data (dict or list) to a JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved data to {file_path}")
    except Exception as e:
        print(f"❌ Failed to write to {file_path}: {e}")
