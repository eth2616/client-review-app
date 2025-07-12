print("Sanity check for Git update")


import os
import streamlit as st


st.write("App loaded successfully ✅")


api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]



try:
    from clients.classify import classify_client
    from ai.openai_summary import summarize_client
    st.write("✅ Modules loaded successfully")
except Exception as e:
    st.error(f"❌ Import failed: {e}")



st.set_page_config(page_title="Client Risk Review", layout="centered")

st.title("🔎 Client Risk Review Tool")

st.markdown("Enter client information below to classify and generate a summary.")

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

if submitted:
    client_data = {
        "name": name,
        "industry": industry,
        "hq_location": hq_location,
        "annual_revenue": annual_revenue,
        "employee_count": employee_count,
        "risk_score": risk_score,
        "watchlist": watchlist,
        "regulatory_issues": regulatory_issues
    }

    with st.spinner("Classifying client..."):
        classification = classify_client(client_data)

    with st.spinner("Generating summary..."):
        summary = summarize_client(client_data)

    st.subheader("🧠 Classification")
    st.json(classification)

    st.subheader("📝 AI Summary")
    st.text_area("Summary Output", summary, height=300)
