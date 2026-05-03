from flask import Flask, request, jsonify
import requests
import uuid
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
LOG_COLLECTOR_URL = "http://localhost:5000/logs"

def send_log(service_name, level, message, correlation_id):
    """Send log to central collector"""
    log_data = {
        "service": service_name,
        "level": level,
        "message": message,
        "correlation_id": correlation_id,
        "timestamp": datetime.now().isoformat()
    }
    try:
        requests.post(LOG_COLLECTOR_URL, json=log_data)
    except:
        # If collector is down, print locally
        print(f"[LOG] {json.dumps(log_data)}")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "user_service"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users - simulated"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    
    # Send INFO log
    send_log("user_service", "INFO", "Fetching all users", correlation_id)
    
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
    
    send_log("user_service", "INFO", f"Found {len(users)} users", correlation_id)
    
    return jsonify({
        "users": users,
        "correlation_id": correlation_id
    }), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    
    send_log("user_service", "INFO", f"Fetching user {user_id}", correlation_id)
    
    # Simulate user not found error
    if user_id > 10:
        send_log("user_service", "ERROR", f"User {user_id} not found", correlation_id)
        return jsonify({"error": "User not found", "correlation_id": correlation_id}), 404
    
    user = {"id": user_id, "name": f"User{user_id}", "email": f"user{user_id}@example.com"}
    
    send_log("user_service", "INFO", f"User {user_id} retrieved successfully", correlation_id)
    
    return jsonify({
        "user": user,
        "correlation_id": correlation_id
    }), 200

@app.route('/users', methods=['POST'])
def create_user():
    """Create new user"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    data = request.get_json()
    
    send_log("user_service", "INFO", f"Creating user: {data.get('name')}", correlation_id)
    
    # Validate input
    if not data.get('name') or not data.get('email'):
        send_log("user_service", "ERROR", "Missing required fields", correlation_id)
        return jsonify({"error": "Name and email required", "correlation_id": correlation_id}), 400
    
    new_user = {
        "id": 100,  # In real app, this would be auto-generated
        "name": data['name'],
        "email": data['email']
    }
    
    send_log("user_service", "INFO", f"User created successfully: {new_user['id']}", correlation_id)
    
    return jsonify({
        "user": new_user,
        "correlation_id": correlation_id
    }), 201

if __name__ == '__main__':
    print("🚀 User Service starting on port 5001...")
    app.run(debug=True, port=5001)