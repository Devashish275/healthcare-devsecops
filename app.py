from flask import Flask, request, jsonify

app = Flask(__name__)
API_KEY = "admin123"
PATIENTS = [{"id": 1, "name": "Dummy Patient", "diagnosis": "Flu"}]

@app.route("/")
def home():
    return "Healthcare Records API"

@app.route("/patients")
def patients():
    if request.headers.get("X-API-KEY") != API_KEY:
        return jsonify(error="unauthorized"), 401
    return jsonify(PATIENTS)

app.run(host="0.0.0.0", port=5000, debug=True)  # nosec B104
