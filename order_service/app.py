from flask import Flask, request, jsonify
import requests
import uuid
from datetime import datetime
import json

app = Flask(__name__)

LOG_COLLECTOR_URL = "http://localhost:5000/logs"
USER_SERVICE_URL = "http://localhost:5001"

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
        print(f"[LOG] {json.dumps(log_data)}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "order_service"}), 200

@app.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    
    send_log("order_service", "INFO", "Fetching all orders", correlation_id)
    
    orders = [
        {"id": 1, "user_id": 1, "product": "Laptop", "amount": 50000},
        {"id": 2, "user_id": 2, "product": "Phone", "amount": 30000}
    ]
    
    send_log("order_service", "INFO", f"Found {len(orders)} orders", correlation_id)
    
    return jsonify({
        "orders": orders,
        "correlation_id": correlation_id
    }), 200

@app.route('/orders', methods=['POST'])
def create_order():
    """Create new order - demonstrates inter-service communication"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    data = request.get_json()
    
    send_log("order_service", "INFO", f"Creating order for user {data.get('user_id')}", correlation_id)
    
    # Call User Service to verify user exists (inter-service communication)
    try:
        user_response = requests.get(
            f"{USER_SERVICE_URL}/users/{data.get('user_id')}",
            headers={'X-Correlation-ID': correlation_id}
        )
        
        if user_response.status_code == 404:
            send_log("order_service", "ERROR", f"User {data.get('user_id')} not found", correlation_id)
            return jsonify({"error": "User not found", "correlation_id": correlation_id}), 404
        
        send_log("order_service", "INFO", f"User verified for order", correlation_id)
        
    except Exception as e:
        send_log("order_service", "ERROR", f"Failed to verify user: {str(e)}", correlation_id)
        return jsonify({"error": "User service unavailable", "correlation_id": correlation_id}), 503
    
    new_order = {
        "id": 100,
        "user_id": data.get('user_id'),
        "product": data.get('product'),
        "amount": data.get('amount')
    }
    
    send_log("order_service", "INFO", f"Order created successfully: {new_order['id']}", correlation_id)
    
    return jsonify({
        "order": new_order,
        "correlation_id": correlation_id
    }), 201

if __name__ == '__main__':
    print("🚀 Order Service starting on port 5002...")
    app.run(debug=True, port=5002)