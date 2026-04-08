# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# ------------------------------
# LoadRunner generator
# ------------------------------
def generate_loadrunner(entries, correlations=[]):
    script = '#include "lrun.h"\n#include "web_api.h"\n\nAction()\n{\n'

    # Add correlations
    for c in correlations:
        script += f'''web_reg_save_param("{c['variable']}",
    "LB=",
    "RB=",
    LAST);\n'''

    # Add requests
    for i, e in enumerate(entries):
        url = e.get("url", "")
        method = e.get("method", "GET").upper()

        # Replace correlated values
        for c in correlations:
            if c['value'] in url:
                url = url.replace(c['value'], f'{{{c["variable"]}}}')

        if method == "GET":
            script += f'''web_url("step{i}",
    "URL={url}",
    LAST);\n'''
        elif method == "POST":
            script += f'''web_submit_data("step{i}",
    "Action={url}",
    "Method=POST",
    LAST);\n'''

    script += "\nreturn 0;\n}"
    return script

# ------------------------------
# JMeter generator placeholder
# ------------------------------
def generate_jmeter(entries):
    # Placeholder content
    return "<jmeter content>"

# ------------------------------
# k6 generator placeholder
# ------------------------------
def generate_k6(entries):
    # Placeholder content
    return "// k6 content"

# ------------------------------
# Basic correlation detection
# ------------------------------
def detect_correlations(entries):
    correlations = []
    for i, e in enumerate(entries):
        url = e.get("url", "")
        if "session" in url.lower():
            correlations.append({"variable": f"session_{i}", "value": "session", "source_step": i})
    return correlations

# ------------------------------
# Routes
# ------------------------------
@app.route('/')
def index():
    return jsonify({"status": "HAR Analyzer backend is running"})

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    har_file = request.files['file']
    try:
        har_json = json.load(har_file)
    except Exception as e:
        return jsonify({"error": "Invalid HAR file", "details": str(e)}), 400

    # Extract requests from HAR
    entries = []
    for e in har_json.get("log", {}).get("entries", []):
        request_data = e.get("request", {})
        entries.append({
            "method": request_data.get("method", "GET"),
            "url": request_data.get("url", "")
        })

    # Detect correlations
    correlations = detect_correlations(entries)

    # Generate scripts
    loadrunner_script = generate_loadrunner(entries, correlations)
    jmeter_script = generate_jmeter(entries)
    k6_script = generate_k6(entries)

    # Return all data
    return jsonify({
        "entries": entries,
        "correlations": correlations,
        "ai": {"message": "AI analysis placeholder"},
        "jmeter": jmeter_script,
        "loadrunner": loadrunner_script,
        "k6": k6_script
    })

# ------------------------------
# Run app
# ------------------------------
if __name__ == "__main__":
    print("Starting HAR Analyzer backend on http://127.0.0.1:5000")
    app.run(debug=True)