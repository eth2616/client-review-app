import json

def summarize_client(client_dict):
    try:
        return f"{client_dict['name']} is a {client_dict['industry']} firm based in {client_dict['hq_location']}."
    except KeyError as e:
        return f"Missing expected field: {e}"

def get_client_json(client_dict):
    try:
        return json.dumps(client_dict, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Invalid client data",
            "details": str(e)
        }, indent=2)

def summarize_client_json(client_dict):
    risk_score = client_dict.get("risk_score")
    subset = {
        "name": client_dict.get("name", "Unknown"),
        "industry": client_dict.get("industry", "Unknown"),
        "risk_score": str(risk_score) if risk_score is not None else "Not available"
    }
    return json.dumps(subset, indent=2)
