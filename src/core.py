# src/core.py
import pandas as pd
from src.api import fetch_flight_data

def calculate_best_hub(df_people, allowed_hubs, price_weight, time_weight):
    """
    Computes the optimal meeting point from a list of allowed hubs 
    based on the travelers' origins and user-defined weights.
    """
    results = []
    
    for _, hub in allowed_hubs.iterrows():
        dest = hub["IATA"]
        total_price = 0
        total_duration = 0
        
        for _, person in df_people.iterrows():
            if person['Origin Airport'] == dest:
                continue
            
            flight = fetch_flight_data(person['Origin Airport'], dest)
            total_price += flight["price"]
            total_duration += flight["duration_hours"]
        
        avg_price = total_price / len(df_people)
        avg_duration = total_duration / len(df_people)
        
        results.append({
            "Destination": dest,
            "Avg Price ($)": round(avg_price, 2),
            "Avg Duration (hrs)": round(avg_duration, 1)
        })
    
    df_results = pd.DataFrame(results)
    
    # Normalization math
    p_min, p_max = df_results['Avg Price ($)'].min(), df_results['Avg Price ($)'].max()
    t_min, t_max = df_results['Avg Duration (hrs)'].min(), df_results['Avg Duration (hrs)'].max()
    
    # Avoid division by zero if all values are identical
    p_denom = (p_max - p_min) if p_max != p_min else 1
    t_denom = (t_max - t_min) if t_max != t_min else 1
    
    df_results['Norm Price'] = (df_results['Avg Price ($)'] - p_min) / p_denom
    df_results['Norm Time'] = (df_results['Avg Duration (hrs)'] - t_min) / t_denom
    
    # Calculate final composite score (lower is better)
    df_results['Score'] = (df_results['Norm Price'] * price_weight) + (df_results['Norm Time'] * time_weight)
    
    return df_results.sort_values(by="Score").drop(columns=['Norm Price', 'Norm Time'])