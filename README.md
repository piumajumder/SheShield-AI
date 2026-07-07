# Women Safety Web App

A Flask-based web application for women's safety assessment using location-based data.

## Setup

1. Make sure you have Python installed
2. The virtual environment is already set up in `.venv/`
3. Dependencies are installed (Flask)

## Running the App

### Option 1: Use the batch file (Windows)
Double-click `run.bat` or run it from command prompt:
```
run.bat
```

### Option 2: Manual command
```
.\.venv\Scripts\python.exe app.py
```

### Option 3: Activate virtual environment first
```
.\.venv\Scripts\Activate.ps1
python app.py
```

## Access the App

Once running, open your browser and go to:
http://127.0.0.1:5000/

## Features

- Location-based safety assessment
- Real-time risk scoring
- Interactive map
- Search by area name
- Current location detection

## Files

- `app.py` - Main Flask application
- `model.py` - Risk prediction logic
- `utils.py` - Utility functions
- `locations_data.json` - Location data
- `templates/index.html` - Main template
- `static/style.css` - Stylesheet
- `requirements.txt` - Python dependencies