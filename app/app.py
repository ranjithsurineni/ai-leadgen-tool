import streamlit as st

# filepath: d:\projects\Ai Leadgen Tool\app\app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import importlib
import src.scraper2
importlib.reload(src.scraper2)
from src.scraper2 import scrape_remoteok_jobs
from src.ranker import rank_leads

st.set_page_config(page_title="AI Leadgen Tool", layout="wide")

st.title("🚀 AI-Driven Lead Prioritization Tool")

# --- Initialize session state ---
if "df_scraped" not in st.session_state:
    st.session_state.df_scraped = pd.DataFrame()

if "df_ranked" not in st.session_state:
    st.session_state.df_ranked = pd.DataFrame()

if "step" not in st.session_state:
    st.session_state.step = "Not Started"

# --- Search Filters Section ---
st.header("🔍 Search Filters")
st.markdown("Configure your search criteria before scraping leads:")

# Keyword input
st.subheader("🔑 Search Keyword")
search_keyword = st.text_input("Enter search keyword (e.g., AI, Python, React, Nurse):", value="AI", help="This will be used to search for jobs on RemoteOK")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📍 Location")
    location_options = ["Any", "US", "Europe", "Worldwide", "Remote"]
    selected_location = st.selectbox("Select location preference:", location_options)
    if selected_location == "Any":
        selected_location = None

with col2:
    st.subheader("💼 Field")
    field_options = ["Any", "AI", "DS", "ML", "Frontend", "Backend", "Nursing", "DevOps", "Mobile"]
    selected_field = st.selectbox("Select field/domain:", field_options)
    if selected_field == "Any":
        selected_field = None

with col3:
    st.subheader("👨‍💼 Experience Level")
    experience_options = ["Any", "Fresher", "Mid", "Senior"]
    selected_experience = st.selectbox("Select experience level:", experience_options)
    if selected_experience == "Any":
        selected_experience = None

# Display selected filters
st.markdown("### 📋 Selected Filters:")
filter_text = [f"🔑 Keyword: {search_keyword}"]
if selected_location:
    filter_text.append(f"📍 Location: {selected_location}")
if selected_field:
    filter_text.append(f"💼 Field: {selected_field}")
if selected_experience:
    filter_text.append(f"👨‍💼 Experience: {selected_experience}")

st.info(" | ".join(filter_text))

st.divider()

# --- Sidebar: Flow Chart ---
with st.sidebar:
    st.header("🧭 Execution Flow")
    steps = {
        "Not Started": "🔲 Not Started",
        "Scraping": "🔄 Scraping Jobs...",
        "Scraped": "✅ Scraping Complete",
        "Ranking": "🔄 Ranking Leads...",
        "Ranked": "✅ Ranking Complete"
    }
    for key, label in steps.items():
        color = "green" if st.session_state.step == key or key in ["Scraped", "Ranked"] and st.session_state.step == "Ranked" else "gray"
        st.markdown(f"<span style='color:{color}'>{label}</span>", unsafe_allow_html=True)

    st.divider()
    st.header("📂 Download CSV Files")

    if os.path.exists("data/leads_raw.csv"):
        st.download_button("📥 Download Raw Leads", open("data/leads_raw.csv", "rb"), file_name="leads_raw.csv")
    else:
        st.warning("❌ Raw CSV not found.")

    if os.path.exists("data/leads_ranked.csv"):
        st.download_button("📥 Download Ranked Leads", open("data/leads_ranked.csv", "rb"), file_name="leads_ranked.csv")
    else:
        st.warning("❌ Ranked CSV not found.")

    st.markdown("---")
    score_threshold = st.slider("🎯 Minimum Score Filter", 0.0, 3.0, 0.0, 0.1)

# --- Main Action Button ---
if st.button("🔄 Scrape & Rank Leads"):
    st.session_state.step = "Scraping"
    with st.spinner("Scraping remote jobs..."):
        df_scraped = scrape_remoteok_jobs(
            keyword=search_keyword,
            location=selected_location,
            field=selected_field,
            experience=selected_experience
        )
        if not df_scraped.empty:
            df_scraped.to_csv("data/leads_raw.csv", index=False)
            st.session_state.df_scraped = df_scraped
            st.session_state.step = "Scraped"
        else:
            st.error("❌ No jobs found matching your criteria. Try adjusting your filters.")
            st.session_state.step = "Not Started"
            st.stop()

    st.session_state.step = "Ranking"
    with st.spinner("Ranking job titles based on AI relevance..."):
        df_ranked = rank_leads("data/leads_raw.csv")
        st.session_state.df_ranked = df_ranked
    st.session_state.step = "Ranked"

    st.success("🎉 Leads successfully scraped and ranked!")

# --- Display Results ---
st.header("📈 Ranked Leads Overview")

import pandas as pd

ranked_csv_path = "data/leads_ranked.csv"
if not os.path.exists(ranked_csv_path):
    st.info("No ranked leads found. Click 'Scrape & Rank Leads' to begin.")
    st.stop()

df_ranked = pd.read_csv(ranked_csv_path)

if df_ranked.empty or "relevance_score" not in df_ranked.columns:
    st.warning("No ranked leads found or 'relevance_score' column missing.")
    st.stop()

df_ranked["relevance_score"] = pd.to_numeric(df_ranked["relevance_score"], errors='coerce')
df_filtered = df_ranked[df_ranked["relevance_score"] >= score_threshold].copy()

st.subheader(f"📊 Top {len(df_filtered)} Leads (Score ≥ {score_threshold})")

# Display columns based on available data
display_columns = ["title", "company", "relevance_score", "link"]
if "location" in df_filtered.columns:
    display_columns.insert(3, "location")
if "field" in df_filtered.columns:
    display_columns.insert(4, "field")
if "experience" in df_filtered.columns:
    display_columns.insert(5, "experience")

st.dataframe(df_filtered[display_columns], use_container_width=True, height=500)

st.markdown("### 🔗 Clickable Job Links")
for _, row in df_filtered.iterrows():
    st.markdown(f"- [{row['title']} @ {row['company']}]({row['link']})")

st.download_button(
    "⬇️ Download Filtered Results",
    df_filtered.to_csv(index=False),
    file_name="leads_filtered.csv"
)

st.markdown("### 📈 Relevance Score Distribution")
st.bar_chart(df_filtered["relevance_score"])

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ by [Rannjih Surinei](https://www.linkedin.com/)")
