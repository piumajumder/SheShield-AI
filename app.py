from flask import Flask, render_template, request, jsonify
from model import predict_risk, predict_risk_by_area_name
from utils import load_locations_data, get_current_time_info
import webbrowser
import threading
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    score = None
    result = None
    color = None
    details = None

    if request.method == "POST":
        hour = int(request.form.get("hour", 0))
        crime = float(request.form.get("crime", 0))
        lighting = int(request.form.get("lighting", 1))
        crowd = int(request.form.get("crowd", 1))

        score, result, color = predict_risk(hour, crime, lighting, crowd)

    # Get all available areas for the frontend
    locations_data = load_locations_data()
    time_info = get_current_time_info()
    
    return render_template("index.html", 
                         score=score, 
                         result=result, 
                         color=color,
                         areas=locations_data['areas'],
                         time_info=time_info)


@app.route("/api/areas", methods=["GET"])
def get_areas():
    """Get all available areas with their data"""
    locations_data = load_locations_data()
    return jsonify(locations_data['areas'])


@app.route("/api/assess-area", methods=["POST"])
def assess_area():
    """
    API endpoint to assess safety for a specific area by name
    Expects JSON: {"area_name": string}
    """
    try:
        data = request.get_json()
        area_name = data.get("area_name")
        detection_method = data.get("detection_method", "Area Search")
        
        if not area_name:
            return jsonify({
                "success": False,
                "message": "Area name is required"
            }), 400
        
        score, status, color, details = predict_risk_by_area_name(area_name, detection_method)
        
        if score is None:
            return jsonify({
                "success": False,
                "message": details  # "Area not found"
            }), 404
        
        return jsonify({
            "success": True,
            "score": score,
            "status": status,
            "color": color,
            "details": details
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


@app.route("/api/time-info", methods=["GET"])
def get_time():
    """Get current time and day information"""
    time_info = get_current_time_info()
    return jsonify(time_info)


@app.route("/api/search-area", methods=["POST"])
def search_area():
    """Search for a specific area by name"""
    try:
        data = request.get_json()
        search_query = data.get("query", "").lower()
        
        locations_data = load_locations_data()
        results = []
        
        for area in locations_data['areas']:
            if search_query in area['name'].lower():
                results.append(area)
        
        return jsonify({
            "success": True,
            "results": results
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


if __name__ == "__main__":
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000/")
    
    threading.Timer(1, open_browser).start()
    app.run(debug=True)