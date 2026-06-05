# src/ui.py
import streamlit as st
import plotly.express as px
import pandas as pd

def render_logistics_map(df_travelers, df_hubs):
    """Generates and displays the interactive Plotly map."""
    st.write("### 🗺️ Current Logistics Map")
    st.write("Blue dots represent your travelers; Orange stars represent your allowed destinations.")
    
    if not df_travelers.empty and not df_hubs.empty:
        # Format travelers for mapping
        df_t_map = df_travelers.copy()
        df_t_map["Type"] = "Traveler"
        df_t_map["Name"] = df_t_map["Name"] + " (" + df_t_map["Origin Airport"] + ")"
        
        # Format hubs for mapping
        df_h_map = df_hubs.copy()
        df_h_map["Type"] = "Potential Destination"
        df_h_map["Name"] = df_h_map["City"] + " (" + df_h_map["IATA"] + ")"
        
        # Combine
        df_map_all = pd.concat([
            df_t_map[["Name", "lat", "lon", "Type"]],
            df_h_map[["Name", "lat", "lon", "Type"]]
        ])
        
        fig = px.scatter_geo(
            df_map_all, 
            lat="lat", lon="lon", 
            color="Type",
            hover_name="Name",
            color_discrete_map={"Traveler": "#1f77b4", "Potential Destination": "#ff7f0e"},
            projection="natural earth"
        )
        fig.update_traces(marker=dict(size=10))
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Add travelers and select at least one airport to display the map.")