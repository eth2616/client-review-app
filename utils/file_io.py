import os
import json
import csv
from datetime import datetime
import pandas as pd

# ── Constants ─────────────────────────────────────────────
CSV_FILE = "classified_clients.csv"

# Define all expected fieldnames for CSV log
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
    "risk_tier",
    "revenue_tier",
    "review_required"
]

# ── JSON Functions ────────────────────────────────────────

def read_json(file_path):
    """Reads a JSON file and returns the parsed data."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return []

def write_json(data, file_path):
    """Writes a list or dictionary to a JSON file with indentation."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved data to {file_path}")
    except Exception as e:
        print(f"❌ Failed to write to {file_path}: {e}")

# ── CSV Functions ─────────────────────────────────────────

def read_csv(file_path):
    """Reads a CSV file and returns a list of dictionaries."""
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return []

def read_clients_from_csv(file_path):
    """Reads client data from CSV and returns a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"⚠️ File {file_path} not found. Returning empty DataFrame.")
        return pd.DataFrame()
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return pd.DataFrame()

def save_client_to_csv(client_data: dict, classification: dict):
    """
    Appends client input and classification result to a CSV file.
    This helps persist a record of all submissions and classifications.
    """
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)

            if not file_exists:
                writer.writeheader()

            row = {
                "timestamp": datetime.utcnow().isoformat(),
                "name": client_data.get("name"),
                "industry": client_data.get("industry"),
                "hq_location": client_data.get("hq_location"),
                "annual_revenue": client_data.get("annual_revenue"),
                "employee_count": client_data.get("employee_count"),
                "risk_score": client_data.get("risk_score"),
                "watchlist": client_data.get("watchlist"),
                "regulatory_issues": client_data.get("regulatory_issues"),
                "risk_tier": classification.get("risk_tier", "N/A"),
                "revenue_tier": classification.get("revenue_tier", "N/A"),
                "review_required": classification.get("review_required", "N/A")
            }

            writer.writerow(row)
        print(f"✅ Appended client to {CSV_FILE}")
    except Exception as e:
        print(f"❌ Failed to write to {CSV_FILE}: {e}")


print(f"📁 Writing CSV to: {os.path.abspath(CSV_FILE)}")
