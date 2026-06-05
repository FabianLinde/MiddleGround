# app.py
import streamlit as st
import pandas as pd

# Custom module imports
from src.api import HUB_DATA, get_origin_info
from src.core import calculate_best_hub
from src.ui import render_logistics_map

# --- Page Config ---
st.set_page_config(page_title="CentriFlight", page_icon="✈️", layout="wide")
st.title("✈️ CentriFlight: Interactive Hub Optimizer")

df_all_hubs = pd.DataFrame(HUB_DATA)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Optimization Settings")
price_weight = st.sidebar.slider("Prioritize Price vs. Time", 0.0, 1.0, 0.5, step=0.1)
time_weight = 1.0 - price_weight

# --- Step 1: Input Travelers ---
st.subheader("1. Add Travelers")
initial_data = pd.DataFrame([
    {"Name": "Alice", "Current City": "New York"},
    {"Name": "Bob", "Current City": "London"},
    {"Name": "Charlie", "Current City": "Berlin"}
])
df_people = st.data_editor(initial_data, num_rows="dynamic", use_container_width=True)

# Parse traveler origins and coordinates safely
traveler_records = []
if not df_people.empty:
    for _, row in df_people.dropna(subset=["Current City"]).iterrows():
        info = get_origin_info(row["Current City"])
        traveler_records.append({
            "Name": row["Name"],
            "City": row["Current City"],
            "Origin Airport": info["IATA"],
            "lat": info["lat"],
            "lon": info["lon"]
        })
df_travelers_processed = pd.DataFrame(traveler_records)

# --- Step 2: Destination Filtering ---
st.write("---")
st.subheader("2. Define Allowed Meeting Destinations")

col1, col2, col3 = st.columns(3)
with col1:
    selected_regions = st.multiselect("Filter by Region", options=df_all_hubs["Region"].unique())
with col2:
    available_countries = df_all_hubs[df_all_hubs["Region"].isin(selected_regions)]["Country"].unique() if selected_regions else df_all_hubs["Country"].unique()
    selected_countries = st.multiselect("Filter by Country", options=available_countries)

# Apply filters
df_filtered_hubs = df_all_hubs.copy()
if selected_regions:
    df_filtered_hubs = df_filtered_hubs[df_filtered_hubs["Region"].isin(selected_regions)]
if selected_countries:
    df_filtered_hubs = df_filtered_hubs[df_filtered_hubs["Country"].isin(selected_countries)]

with col3:
    final_hubs = st.multiselect(
        "Allowed Airports", 
        options=df_filtered_hubs["IATA"].tolist(),
        default=df_filtered_hubs["IATA"].tolist()
    )

df_active_candidates = df_all_hubs[df_all_hubs["IATA"].isin(final_hubs)].copy()

# --- Step 3: Map Display ---
render_logistics_map(df_travelers_processed, df_active_candidates)

# --- Step 4: Run Optimization Engine ---
st.write("---")
if st.button("🚀 Optimize Meeting Hub", type="primary"):
    if df_travelers_processed.empty or df_active_candidates.empty:
        st.error("Please add travelers and verify that at least one destination hub is checked.")
    else:
        with st.spinner("Crunching routing matrices..."):
            df_results = calculate_best_hub(
                df_travelers_processed, 
                df_active_candidates, 
                price_weight, 
                time_weight
            )
            
            st.success("Analysis Complete!")
            st.subheader("🏆 Optimal Destinations Ranked")
            st.dataframe(df_results, use_container_width=True)
            
            best_dest = df_results.iloc[0]['Destination']
            st.balloons()
            st.info(f"**Recommendation:** Plan your meeting in **{best_dest}**!")