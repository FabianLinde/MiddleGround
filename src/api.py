# src/api.py

# Static database of global hubs
HUB_DATA = [
    {"IATA": "LHR", "City": "London", "Country": "UK", "Region": "Europe", "lat": 51.4700, "lon": -0.4543},
    {"IATA": "CDG", "City": "Paris", "Country": "France", "Region": "Europe", "lat": 49.0097, "lon": 2.5479},
    {"IATA": "FRA", "City": "Frankfurt", "Country": "Germany", "Region": "Europe", "lat": 50.0379, "lon": 8.5622},
    {"IATA": "JFK", "City": "New York", "Country": "USA", "Region": "North America", "lat": 40.6413, "lon": -73.7781},
    {"IATA": "LAX", "City": "Los Angeles", "Country": "USA", "Region": "North America", "lat": 33.9416, "lon": -118.4085},
    {"IATA": "DXB", "City": "Dubai", "Country": "UAE", "Region": "Middle East", "lat": 25.2532, "lon": 55.3657},
    {"IATA": "SIN", "City": "Singapore", "Country": "Singapore", "Region": "Asia", "lat": 1.3644, "lon": 103.9915},
    {"IATA": "HND", "City": "Tokyo", "Country": "Japan", "Region": "Asia", "lat": 35.5494, "lon": 139.7798},
]

MOCK_ORIGINS = {
    "New York": {"IATA": "JFK", "lat": 40.6413, "lon": -73.7781},
    "London": {"IATA": "LHR", "lat": 51.4700, "lon": -0.4543},
    "Berlin": {"IATA": "BER", "lat": 52.3667, "lon": 13.5033},
    "Singapore": {"IATA": "SIN", "lat": 1.3644, "lon": 103.9915}
}

def get_origin_info(city_string):
    """Fetches IATA code and coordinates for a user's starting city."""
    return MOCK_ORIGINS.get(city_string, {"IATA": "JFK", "lat": 40.6413, "lon": -73.7781})

def fetch_flight_data(origin, destination):
    """Calls live Flight API to get real prices and durations."""
    # Placeholder mock data; replace with real API requests later
    return {"price": 450, "duration_hours": 7.5}