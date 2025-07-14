# --- Classify client data based on business rules ---

def classify_client(client_data):
    """
    Classifies a client into risk and revenue tiers and determines if further review is required.
    
    Parameters:
        client_data (dict): Dictionary containing client attributes like revenue, risk score, etc.
    
    Returns:
        dict: Classification result including risk_tier, revenue_tier, and review_required.
    """

    # --- Risk Tier Classification ---
    # Based on risk score thresholds
    risk_score = client_data.get("risk_score", 0)
    if risk_score >= 0.7:
        risk_tier = "High Risk"
    elif risk_score >= 0.4:
        risk_tier = "Moderate Risk"
    else:
        risk_tier = "Low Risk"

    # --- Revenue Tier Classification ---
    # Based on annual revenue in billions
    revenue = client_data.get("annual_revenue", 0)
    if revenue >= 10:
        revenue_tier = "Enterprise"
    elif revenue >= 1:
        revenue_tier = "Mid-Market"
    else:
        revenue_tier = "Small Business"

    # --- Review Requirement ---
    # A review is required if:
    # - The client is high risk
    # - The client is on the watchlist
    # - The client has documented regulatory issues
    watchlist = client_data.get("watchlist", False)
    has_issues = bool(client_data.get("regulatory_issues", "").strip())

    review_required = (
        risk_tier == "High Risk" or
        watchlist or
        has_issues
    )

    # --- Final Classification Dictionary ---
    return {
        "risk_tier": risk_tier,
        "revenue_tier": revenue_tier,
        "review_required": review_required
    }
