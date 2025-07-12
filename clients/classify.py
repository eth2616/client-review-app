def classify_client(client):
    risk_score = client.get("risk_score", 0)
    revenue = client.get("annual_revenue", 0)

    risk_tier = (
        "High Risk" if risk_score > 0.8 else
        "Moderate Risk" if risk_score > 0.5 else
        "Low Risk"
    )

    revenue_tier = (
        "Enterprise" if revenue > 50 else
        "Mid-Market" if revenue > 10 else
        "Small Business"
    )

    return {
        "name": client["name"],
        "risk_tier": risk_tier,
        "revenue_tier": revenue_tier,
        "review_required": risk_tier == "High Risk"
    }
