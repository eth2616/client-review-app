# --- Standard & External Imports ---
import os
from dotenv import load_dotenv  # Helps load environment variables from .env
import streamlit as st

# --- Internal Imports ---
from utils.file_io import save_client_to_csv, read_clients_from_csv

# --- Load Environment Variables ---
load_dotenv()  # Load .env file if it exists (for local dev)

# --- Retrieve API Key ---
# Priority: .env (local) > Streamlit Secrets (cloud)
try:
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found in environment or Streamlit secrets.")

# --- Streamlit Debug Check ---
st.write("✅ App loaded successfully")

# --- Load AI Modules ---
try:
    from clients.classify import classify_client
    from ai.openai_summary import summarize_client
    st.write("✅ Modules loaded successfully")
except Exception as e:
    st.error(f"❌ Failed to import core modules: {e}")

# --- Streamlit Page Settings ---
st.set_page_config(page_title="Client Risk Review", layout="centered")
st.title("🔎 Client Risk Review Tool")
st.markdown("Enter client information below to classify and generate a summary.")

# --- Input Form ---
with st.form("client_form"):
    name = st.text_input("Client Name")
    industry = st.text_input("Industry")
    hq_location = st.text_input("HQ Location")
    annual_revenue = st.number_input("Annual Revenue (in billions)", min_value=0.0)
    employee_count = st.number_input("Employee Count", min_value=0)
    risk_score = st.slider("Risk Score", 0.0, 1.0, 0.5)
    watchlist = st.checkbox("Watchlist?", value=False)
    regulatory_issues = st.text_area("Regulatory Issues (if any)", value="")

    # Submit button triggers the logic below
    submitted = st.form_submit_button("Classify & Summarize")

# --- If Submitted: Classify, Summarize, Save ---
if submitted:
    # Collect all form inputs into one dictionary
    client_data = {
        "name": name,
        "industry": industry,
        "hq_location": hq_location,
        "annual_revenue": annual_revenue,
        "employee_count": employee_count,
        "risk_score": risk_score,
        "watchlist": watchlist,
        "regulatory_issues": regulatory_issues,
    }

    # --- AI Classification ---
    with st.spinner("Classifying client..."):
        classification = classify_client(client_data)
        save_client_to_csv(client_data, classification)  # Save to CSV log

    # --- AI Summary Generation ---
    with st.spinner("Generating summary..."):
        summary = summarize_client(client_data)

    # --- Display Results ---
    st.subheader("🧠 Classification")
    st.json(classification)

    st.subheader("📝 AI Summary")
    st.text_area("Summary Output", summary, height=300)

# --- Show CSV Log of All Clients ---
st.subheader("📊 All Clients Logged")
all_clients = read_clients_from_csv("classified_clients.csv")

# Safely check if it's a non-empty DataFrame
if hasattr(all_clients, "empty") and not all_clients.empty:
    st.dataframe(all_clients)
else:
    st.info("No client data found yet.")
