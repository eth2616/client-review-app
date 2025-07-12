from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables (e.g., your OpenAI API key)
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_summary(client_data):
    prompt_lines = [
        "You are a banking risk analyst. Summarize this high-risk client for an internal review memo:\n",
        f"Name: {client_data['name']}",
        f"Industry: {client_data['industry']}",
        f"HQ Location: {client_data['hq_location']}",
        f"Annual Revenue: {client_data['annual_revenue']} billion",
        f"Employee Count: {client_data['employee_count']}",
        f"Risk Score: {client_data['risk_score']}"
    ]

    if client_data.get("watchlist") is not None:
        prompt_lines.append(f"On Watchlist: {'Yes' if client_data['watchlist'] else 'No'}")
    if client_data.get("regulatory_issues"):
        prompt_lines.append(f"Regulatory Issues: {client_data['regulatory_issues']}")

    prompt = "\n".join(prompt_lines)

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content
        return content.strip() if content else "❌ No response content received."
    except Exception as e:
        return f"❌ Error generating summary: {e}"

# Alias for compatibility with other parts of the project
summarize_client = generate_ai_summary
