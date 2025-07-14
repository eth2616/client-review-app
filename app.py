# --- Standard & External Imports ---
import streamlit as st
from utils.config import get_openai_api_key  # ← NEW: Centralized config
from utils.file_io import save_client_to_csv, read_clients_from_csv

# --- Internal Imports ---
try:
    from clients.classify import classify_client
    from ai.openai_summary import summarize_client
    st.write("✅ Modules loaded successfully")
except Exception as e:
    st.error(f"❌ Failed to import core modules: {e}")

# --- Load API Key ---
api_key = get_openai_api_key()
if not api_key:
    st.error("❌ OPENAI_API_KEY not found.")

# --- Streamlit Page Setup ---
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

    submitted = st.form_submit_button("Classify & Summarize")

# --- On Submit ---
if submitted:
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

    with st.spinner("Classifying client..."):
        classification = classify_client(client_data)
        save_client_to_csv(client_data, classification)

    with st.spinner("Generating summary..."):
        summary = summarize_client(client_data, classification)

    st.subheader("🧠 Classification")
    st.json(classification)

    st.subheader("📝 AI Summary")
    st.text_area("Summary Output", summary, height=300)

# --- Display CSV Log ---
st.subheader("📊 All Clients Logged")
all_clients = read_clients_from_csv("classified_clients.csv")

if hasattr(all_clients, "empty") and not all_clients.empty:
    st.dataframe(all_clients)
else:
    st.info("No client data found yet.")
