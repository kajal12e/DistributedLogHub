from flask import Flask, request, jsonify
import requests
import uuid
from datetime import datetime
import json
import random

app = Flask(__name__)

import os
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
        print(f"[LOG] {json.dumps(log_data)}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "product_service"}), 200

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    
    send_log("product_service", "INFO", "Fetching all products", correlation_id)
    
    # Simulate occasional errors (10% chance)
    if random.random() < 0.1:
        send_log("product_service", "ERROR", "Database connection timeout", correlation_id)
        return jsonify({"error": "Service temporarily unavailable", "correlation_id": correlation_id}), 503
    
    products = [
        {"id": 1, "name": "Laptop", "price": 50000, "stock": 10},
        {"id": 2, "name": "Phone", "price": 30000, "stock": 25},
        {"id": 3, "name": "Headphones", "price": 5000, "stock": 50}
    ]
    
    send_log("product_service", "INFO", f"Found {len(products)} products", correlation_id)
    
    return jsonify({
        "products": products,
        "correlation_id": correlation_id
    }), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product"""
    correlation_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    
    send_log("product_service", "INFO", f"Fetching product {product_id}", correlation_id)
    
    if product_id > 100:
        send_log("product_service", "WARNING", f"Product {product_id} not found", correlation_id)
        return jsonify({"error": "Product not found", "correlation_id": correlation_id}), 404
    
    product = {
        "id": product_id,
        "name": f"Product{product_id}",
        "price": random.randint(1000, 100000),
        "stock": random.randint(0, 100)
    }
    
    send_log("product_service", "INFO", f"Product {product_id} retrieved", correlation_id)
    
    return jsonify({
        "product": product,
        "correlation_id": correlation_id
    }), 200

if __name__ == '__main__':
    print("🚀 Product Service starting on port 5003...")
    app.run(debug=True, port=5003)