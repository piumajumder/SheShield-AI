# 🛡️ SheShield AI

**SheShield AI** is a Flask-based web application that helps you check how safe an area is before you head there. It combines location data — crime frequency, lighting, crowd density, and time of day — into a simple risk score, shows it on an interactive map, and surfaces emergency helplines when you need them.

🔗 **Live demo:** [she-shield-ai-kappa.vercel.app](https://she-shield-ai-kappa.vercel.app)


---

## ✨ Features

- **📍 Location detection** — use your device GPS to instantly find the nearest known area, or search by name
- **📊 Risk scoring** — a weighted score combining crime frequency, lighting conditions, crowd density, and time of day
- **🗺️ Interactive map** — every area plotted on a live map, color-coded green / amber / red by risk level
- **🚨 Emergency help** — local helpline numbers and quick safety tips shown alongside every result
- **🕐 Live clock** — current date and time, since risk depends on time of day
- **📱 Responsive UI** — works on desktop and mobile

---

## 🧱 Tech Stack

| Layer      | Tech                                   |
|------------|-----------------------------------------|
| Backend    | Python, Flask                          |
| Frontend   | HTML, CSS, vanilla JavaScript          |
| Map        | [Leaflet.js](https://leafletjs.com/) + OpenStreetMap tiles |
| Icons      | [Font Awesome](https://fontawesome.com/) |
| Data       | Static JSON (`locations_data.json`)    |

---

## 📂 Project Structure

```
SheShield-AI/
├── app.py                 # Flask app & routes
├── model.py                # Risk-scoring logic
├── utils.py                 # Helpers (location matching, time info, etc.)
├── locations_data.json     # Area dataset (coordinates, crime, lighting, crowd)
├── requirements.txt         # Python dependencies
├── run.bat                  # Windows one-click launcher
├── templates/
│   └── index.html           # Main page
├── static/
│   └── style.css             # Stylesheet
└── tests/                   # Test suite
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### 1. Clone the repo
```bash
git clone https://github.com/piumajumder/SheShield-AI.git
cd SheShield-AI
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

Windows users can also just double-click **`run.bat`**.

### 5. Open it in your browser
```
http://127.0.0.1:5000/
```

---

## 🔌 API Endpoints

| Method | Endpoint               | Description                                   |
|--------|--------------------------|------------------------------------------------|
| GET    | `/`                       | Renders the main page                          |
| GET    | `/api/areas`              | Returns all areas with their safety data       |
| POST   | `/api/assess-area`        | Assess risk for an area by name → `{ area_name, detection_method }` |
| POST   | `/api/search-area`        | Search areas by (partial) name → `{ query }`   |
| GET    | `/api/time-info`          | Returns current date/time info                |

**Example — assess an area:**
```bash
curl -X POST http://127.0.0.1:5000/api/assess-area \
  -H "Content-Type: application/json" \
  -d '{"area_name": "Central Business District"}'
```

---

## 🧮 How Risk Is Calculated

Each area gets a score between `0` and `1`, built from:

- **Time of day** — late night / early morning adds risk
- **Crime frequency** — weighted most heavily
- **Lighting conditions** — poorly lit areas score higher risk
- **Crowd density** — sparser crowds score higher risk

| Score        | Status     |
|--------------|------------|
| `< 0.3`      | 🟢 Safe     |
| `0.3 – 0.6`  | 🟡 Moderate |
| `> 0.6`      | 🔴 Unsafe   |

> This is a heuristic score for awareness, not a guarantee of safety. Always use your own judgment and trust your instincts.

---

## 🧪 Running Tests

```bash
python -m pytest tests/
```

---

## 🤝 Contributing

Contributions are welcome! To propose a change:

1. Fork the repo and create a branch (`git checkout -b feature/my-feature`)
2. Make your changes and commit (`git commit -m "Add my feature"`)
3. Push to your branch (`git push origin feature/my-feature`)
4. Open a Pull Request

---

## ⚠️ Disclaimer

SheShield AI is a demonstration project. The safety data and risk scores are for informational purposes only and should not be relied on as a substitute for professional safety advice, local knowledge, or emergency services.

---

## 📄 License

No license has been specified yet. Until one is added, all rights are reserved by the repository owner.
