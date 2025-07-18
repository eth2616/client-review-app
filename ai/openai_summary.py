from openai import OpenAI
from utils.config import get_openai_api_key  # Centralized config

api_key = get_openai_api_key()
openai_client = OpenAI(api_key=api_key)

def generate_ai_summary(client_data, classification):
    """
    Generates an AI-written summary of a client's risk profile.
    Now dynamically reflects the correct risk tier.
    """
    prompt_lines = [
        "You are a banking risk analyst. Write an internal memo summarizing the following client:\n",
        f"Name: {client_data['name']}",
        f"Industry: {client_data['industry']}",
        f"HQ Location: {client_data['hq_location']}",
        f"Annual Revenue: {client_data['annual_revenue']} billion",
        f"Employee Count: {client_data['employee_count']}",
        f"Risk Score: {client_data['risk_score']}",
        f"Risk Tier: {classification['risk_tier']}",  # <- dynamically added
        f"Revenue Tier: {classification['revenue_tier']}",
        f"Review Required: {'Yes' if classification['review_required'] else 'No'}",
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


# Alias for compatibility
summarize_client = generate_ai_summary
