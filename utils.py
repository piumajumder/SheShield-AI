import json
import math
from datetime import datetime

def load_locations_data():
    """Load locations data from JSON file"""
    try:
        with open('locations_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"areas": []}

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula"""
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def find_nearest_area(latitude, longitude, max_distance=2):
    """Find the nearest area to given coordinates"""
    locations = load_locations_data()
    nearest_area = None
    min_distance = float('inf')
    
    for area in locations['areas']:
        distance = calculate_distance(latitude, longitude, area['latitude'], area['longitude'])
        if distance < min_distance and distance <= max_distance:
            min_distance = distance
            nearest_area = area
    
    return nearest_area, min_distance

def get_current_time_info():
    """Get current time and day information"""
    now = datetime.now()
    return {
        "hour": now.hour,
        "minute": now.minute,
        "day": now.strftime("%A"),
        "date": now.strftime("%Y-%m-%d"),
        "timestamp": now.isoformat()
    }

def normalize_lighting(lighting_text):
    """Normalize lighting condition to numeric value"""
    mapping = {
        "Good": 1,
        "Moderate": 0.5,
        "Poor": 0
    }
    return mapping.get(lighting_text, 0)

def normalize_crowd(crowd_text):
    """Normalize crowd density to numeric value"""
    mapping = {
        "Very High": 1,
        "High": 0.8,
        "Medium": 0.5,
        "Low": 0.2
    }
    return mapping.get(crowd_text, 0)
