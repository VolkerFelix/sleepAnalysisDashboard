from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime
import os
import uuid

from test_data import create_test_sleep_data

app = Flask(__name__)

# Configure the API endpoint
API_HOST = os.environ.get('API_HOST', 'http://localhost:8000')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Forward sleep data to the analysis API and return results"""
    try:
        sleep_data = create_test_sleep_data(
            duration_hours=float(request.form.get('duration', 8)),
            quality=request.form.get('quality', 'good')
        )
        
        # Create the complete analysis request
        analysis_request = {
            "sleep_data": json.loads(sleep_data.json()),
            "include_metrics": True,
            "include_patterns": True,
            "include_stages": True,
            "user_id": request.form.get('user_id', f"user-{uuid.uuid4()}"),
            "session_id": f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        }
        
        # Determine which endpoint to use based on analysis type
        is_conversational = request.form.get('conversational', 'false').lower() == 'true'
        endpoint = "/api/analyze/conversational" if is_conversational else "/api/analyze"
        
        # Call the API
        response = requests.post(
            f"{API_HOST}{endpoint}", 
            json=analysis_request
        )
        
        # Return the result
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/validate', methods=['POST'])
def validate():
    """Validate sleep data using the validation API"""
    try:
        sleep_data = create_test_sleep_data(
            duration_hours=float(request.form.get('duration', 8)),
            quality=request.form.get('quality', 'good')
        )
        
        # Call the validation API
        response = requests.post(
            f"{API_HOST}/api/validate", 
            json=json.loads(sleep_data.json())
        )
        
        # Return the result
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Check the health of the API service"""
    try:
        response = requests.get(f"{API_HOST}/health")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e), "status": "Service unreachable"}), 500

@app.route('/stage_types')
def stage_types():
    """Get all supported sleep stage types"""
    try:
        response = requests.get(f"{API_HOST}/api/stage_types")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)