import json
import csv
import os
from datetime import datetime

# ── JSON FUNCTIONS ─────────────────────────────

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

# ── CSV FUNCTION ───────────────────────────────

CSV_FILE = "classified_clients.csv"
FIELDNAMES = [
    "timestamp",
    "name",
    "industry",
    "hq_location",
    "annual_revenue",
    "employee_count",
    "risk_score",
    "watchlist",
    "regulatory_issues",
    "classification"
]


def read_csv(file_path):
    """Reads a CSV file and returns the parsed data."""
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return []



def save_client_to_csv(client_data: dict, classification: dict):
    """Appends client submission and classification to CSV."""
    file_exists = os.path.isfile(CSV_FILE)
    try:
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)

            if not file_exists:
                writer.writeheader()

            row = {
                "timestamp": datetime.utcnow().isoformat(),
                **client_data,
                "classification": classification.get("category", "N/A")
            }
            writer.writerow(row)
        print(f"✅ Appended client to {CSV_FILE}")
    except Exception as e:
        print(f"❌ Failed to write to {CSV_FILE}: {e}")


import pandas as pd

def read_clients_from_csv(file_path):
    """Reads client data from a CSV file and returns a DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"⚠️ File {file_path} not found. Returning empty DataFrame.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return pd.DataFrame()
