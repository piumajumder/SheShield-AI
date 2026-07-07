from utils import find_nearest_area, get_current_time_info, normalize_lighting, normalize_crowd
from datetime import datetime


def _get_risk_score(area, hour):
    """Calculate the risk score for a given area and hour."""
    score = 0

    if hour >= 20 or hour <= 5:
        score += 0.25
    elif hour >= 18 or hour <= 7:
        score += 0.15

    score += area['crime_frequency'] * 0.4

    lighting_score = normalize_lighting(area['lighting_conditions'])
    score += (1 - lighting_score) * 0.2

    crowd_score = normalize_crowd(area['crowd_density'])
    score += (1 - crowd_score) * 0.1

    return round(score, 2)


def _get_risk_status(score):
    """Translate a numeric risk score into a status and color."""
    if score < 0.3:
        return "SAFE", "green"
    if score < 0.6:
        return "MODERATE", "yellow"
    return "UNSAFE", "red"


def _build_safety_advice(status):
    """Create a short safety tip for the current status."""
    if status == "SAFE":
        return "Area appears safe. Stay aware and continue your route."
    if status == "MODERATE":
        return "Moderate risk. Consider avoiding this area at night or stay in well-lit sections."
    return "High risk. Avoid the route especially after dark and choose a safer nearby path."


def _build_emergency_help():
    """Create a small emergency-help section for the UI."""
    return {
        "title": "Emergency Help & Helplines",
        "contacts": [
            {"label": "Emergency Services", "value": "Call 112 or your local emergency number immediately if you feel unsafe."},
            {"label": "Women Helpline", "value": "In India, call 181 for women safety assistance and support."},
            {"label": "Police Help", "value": "Call 100 for police assistance."},
            {"label": "Trusted Contact", "value": "Share your live location with someone you trust."},
            {"label": "Safe Place", "value": "Move to a busy stop, station, hospital, or well-lit public place."}
            

        ],
        "tips": [
            "If you are in immediate danger, call emergency services right away.",
            "If you need help but cannot speak, send a message to the emergency services."
        ]
    }


def predict_risk(hour, crime_rate, lighting, crowd):
    """Original risk prediction function"""
    score = 0

    if hour >= 20 or hour <= 5:
        score += 0.3

    score += crime_rate * 0.4

    if lighting == 0:
        score += 0.2

    if crowd == 0:
        score += 0.1

    status, color = _get_risk_status(score)

    return round(score, 2), status, color


def predict_risk_by_location(latitude, longitude):
    """
    Predict safety risk based on location coordinates
    Combines time-of-day factors with area-specific data
    """
    area, distance = find_nearest_area(latitude, longitude)

    if area is None:
        return None, "Area data not available", "gray"

    time_info = get_current_time_info()
    hour = time_info["hour"]

    score = _get_risk_score(area, hour)
    status, color = _get_risk_status(score)
    advice = _build_safety_advice(status)

    locations_data = {"areas": []}
    try:
        from utils import load_locations_data
        locations_data = load_locations_data()
    except Exception:
        pass

    details = {
        "area_name": area['name'],
        "latitude": area['latitude'],
        "longitude": area['longitude'],
        "detection_method": "GPS Location",
        "risk_score": round(score, 2),
        "status": status,
        "color": color,
        "crime_frequency": area['crime_frequency'],
        "incident_types": area['incident_types'],
        "lighting": area['lighting_conditions'],
        "crowd_density": area['crowd_density'],
        "advice": advice,
        "emergency_help": _build_emergency_help()
    }

    return round(score, 2), status, color, details


def predict_risk_by_area_name(area_name, detection_method="Area Search"):
    """
    Predict safety risk based on area name
    """
    from utils import load_locations_data

    locations_data = load_locations_data()
    area = None
    for a in locations_data['areas']:
        if a['name'].lower() == area_name.lower():
            area = a
            break

    if area is None:
        return None, "Area not found", "gray", None

    time_info = get_current_time_info()
    hour = time_info["hour"]

    score = _get_risk_score(area, hour)
    status, color = _get_risk_status(score)
    advice = _build_safety_advice(status)

    details = {
        "area_name": area['name'],
        "latitude": area['latitude'],
        "longitude": area['longitude'],
        "detection_method": detection_method,
        "risk_score": round(score, 2),
        "status": status,
        "color": color,
        "crime_frequency": area['crime_frequency'],
        "incident_types": area['incident_types'],
        "lighting": area['lighting_conditions'],
        "crowd_density": area['crowd_density'],
        "advice": advice,
        "emergency_help": _build_emergency_help()
    }

    return round(score, 2), status, color, details
