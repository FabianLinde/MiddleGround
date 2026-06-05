# src/ui.py
import streamlit as st
import plotly.express as px
import pandas as pd

def render_logistics_map(df_travelers, df_hubs):
    """Generates and displays the interactive Plotly map."""
    st.write("### 🗺️ Current Logistics Map")
    st.write("🔵 Blue circles represent your travelers; 🟠 Orange stars represent your allowed destinations.")
    
    if not df_travelers.empty and not df_hubs.empty:
        # Format travelers for mapping
        df_t_map = df_travelers.copy()
        df_t_map["Type"] = "Traveler"
        df_t_map["Hover_Text"] = df_t_map["Name"] + " (" + df_t_map["Origin Airport"] + ")"
        
        # Format hubs for mapping
        df_h_map = df_hubs.copy()
        df_h_map["Type"] = "Potential Destination"
        df_h_map["Hover_Text"] = df_h_map["City"] + " (" + df_h_map["IATA"] + ")"
        
        # Combine
        df_map_all = pd.concat([
            df_t_map[["Hover_Text", "lat", "lon", "Type"]],
            df_h_map[["Hover_Text", "lat", "lon", "Type"]]
        ], ignore_index=True)
        
        fig = px.scatter_geo(
            df_map_all, 
            lat="lat", lon="lon", 
            color="Type",
            hover_name="Hover_Text",
            color_discrete_map={
                "Traveler": "#3B82F6",  # Modern blue
                "Potential Destination": "#F97316"  # Modern orange
            },
            projection="natural earth"
        )
        
        # Update traces for better styling
        for trace in fig.data:
            if "Traveler" in trace.name:
                trace.marker.size = 15
                trace.marker.line = dict(width=2, color="white")
                trace.marker.opacity = 0.85
            else:
                trace.marker.size = 18
                trace.marker.symbol = "star"
                trace.marker.line = dict(width=2, color="white")
                trace.marker.opacity = 0.9
        
        fig.update_layout(
            height=550,
            margin=dict(r=0, t=0, l=0, b=0),
            geo=dict(
                bgcolor="rgba(240, 248, 255, 0.3)",
                showland=True,
                landcolor="rgb(243, 243, 243)",
                coastcolor="rgb(204, 204, 204)",
                projection_type="natural earth",
                showocean=True,
                oceancolor="rgb(230, 245, 255)"
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="rgba(0, 0, 0, 0.2)",
                borderwidth=1
            ),
            hovermode="closest"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Add travelers and select at least one airport to display the map.")