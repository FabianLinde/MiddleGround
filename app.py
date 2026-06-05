import streamlit as st
import pandas as pd
import time

# --- Mock API Functions (Replace these with your actual API integration) ---
def get_nearest_airport(location_string):
    """
    Given a city name, return the nearest IATA code.
    In production, use geopy + airportsdata or Amadeus Airport API.
    """
    mock_airports = {"New York": "JFK", "London": "LHR", "Paris": "CDG", "Tokyo": "NRT"}
    return mock_airports.get(location_string, "JFK")

def fetch_flight_data(origin, destination):
    """
    Calls your Flight API (e.g., Amadeus) to get real price and duration.
    """
    # Placeholder mock data
    return {"price": 400, "duration_hours": 8.5}


# --- UI Setup ---
st.set_page_config(page_title="Fly-to-Meet Optimizer", page_icon="✈️", layout="wide")
st.title("✈️ Central Hub & Flight Optimizer")
st.write("Find the fairest, cheapest, or fastest meeting point for your distributed team.")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Optimization Settings")
price_weight = st.sidebar.slider(
    "Prioritize Price vs. Time", 
    min_value=0.0, max_value=1.0, value=0.5, step=0.1,
    help="0.0 = Purely quickest time | 1.0 = Purely cheapest price"
)
time_weight = 1.0 - price_weight

# --- Step 1: User Data Input ---
st.subheader("1. Who is traveling and from where?")
input_method = st.radio("Choose Input Method:", ("Interactive Table", "Upload CSV"))

# Standardizing data structure
df_people = pd.DataFrame(columns=["Name", "Current City"])

if input_method == "Interactive Table":
    # Seed with some example data
    initial_data = pd.DataFrame([
        {"Name": "Alice", "Current City": "New York"},
        {"Name": "Bob", "Current City": "London"}
    ])
    df_people = st.data_editor(initial_data, num_rows="dynamic", use_container_width=True)

elif input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload your CSV file (Columns required: 'Name', 'Current City')", type=["csv"])
    if uploaded_file is not None:
        df_people = pd.read_csv(uploaded_file)
        st.dataframe(df_people, use_container_width=True)

# --- Step 2 & 3: Computation ---
if st.button("🚀 Calculate Best Meeting Point", type="primary"):
    if df_people.empty:
        st.error("Please add at least one traveler.")
    else:
        with st.spinner("Analyzing routes and fetching live data..."):
            
            # Find origin airports
            df_people['Origin Airport'] = df_people['Current City'].apply(get_nearest_airport)
            
            # Defined sample candidate hubs to test as meeting locations
            candidate_destinations = ["LHR", "CDG", "JFK"] 
            results = []
            
            # Nested loop to calculate metrics
            for dest in candidate_destinations:
                total_price = 0
                total_duration = 0
                
                for _, person in df_people.iterrows():
                    # Avoid searching if they live at the destination
                    if person['Origin Airport'] == dest:
                        continue
                    
                    flight = fetch_flight_data(person['Origin Airport'], dest)
                    total_price += flight["price"]
                    total_duration += flight["duration_hours"]
                
                # Average metrics per person
                avg_price = total_price / len(df_people)
                avg_duration = total_duration / len(df_people)
                
                results.append({
                    "Destination": dest,
                    "Avg Price ($)": round(avg_price, 2),
                    "Avg Duration (hrs)": round(avg_duration, 1)
                })
            
            # Convert to results dataframe
            df_results = pd.DataFrame(results)
            
            # Standard normalization logic to apply our weights
            # (In production, avoid dividing by zero if min==max)
            df_results['Norm Price'] = (df_results['Avg Price ($)'] - df_results['Avg Price ($)'].min()) / (df_results['Avg Price ($)'].max() - df_results['Avg Price ($)'].min() + 1)
            df_results['Norm Time'] = (df_results['Avg Duration (hrs)'] - df_results['Avg Duration (hrs)'].min()) / (df_results['Avg Duration (hrs)'].max() - df_results['Avg Duration (hrs)'].min() + 1)
            
            # Calculate final score (lower is better)
            df_results['Score'] = (df_results['Norm Price'] * price_weight) + (df_results['Norm Time'] * time_weight)
            df_results = df_results.sort_values(by="Score").drop(columns=['Norm Price', 'Norm Time'])
            
            # Output Display
            st.success("Analysis Complete!")
            st.subheader("🏆 Optimal Destinations Ranked")
            st.dataframe(df_results, use_container_width=True)
            
            best_destination = df_results.iloc[0]['Destination']
            st.balloons()
            st.info(f"**Recommendation:** You should meet in **{best_destination}**!")