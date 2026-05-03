from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict

app = Flask(__name__)

# Storage file
LOGS_FILE = "logs_database.json"

def load_logs():
    """Load logs from JSON file"""
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_logs(logs):
    """Save logs to JSON file"""
    with open(LOGS_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "log_collector"}), 200

@app.route('/logs', methods=['POST'])
def collect_log():
    """Receive and store logs from services"""
    log_data = request.get_json()
    
    # Add unique ID and server timestamp
    log_data['log_id'] = f"log_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    log_data['server_timestamp'] = datetime.now().isoformat()
    
    # Load existing logs
    logs = load_logs()
    logs.append(log_data)
    save_logs(logs)
    
    print(f"📝 Log received: {log_data['service']} - {log_data['level']} - {log_data['message']}")
    
    return jsonify({"status": "logged", "log_id": log_data['log_id']}), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retrieve logs with filtering"""
    logs = load_logs()
    
    # Filter parameters
    service = request.args.get('service')
    level = request.args.get('level')
    correlation_id = request.args.get('correlation_id')
    limit = int(request.args.get('limit', 100))
    
    # Apply filters
    filtered_logs = logs
    
    if service:
        filtered_logs = [log for log in filtered_logs if log.get('service') == service]
    
    if level:
        filtered_logs = [log for log in filtered_logs if log.get('level') == level]
    
    if correlation_id:
        filtered_logs = [log for log in filtered_logs if log.get('correlation_id') == correlation_id]
    
    # Sort by timestamp (newest first)
    filtered_logs = sorted(filtered_logs, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Limit results
    filtered_logs = filtered_logs[:limit]
    
    return jsonify({
        "total": len(filtered_logs),
        "logs": filtered_logs
    }), 200

@app.route('/logs/search', methods=['GET'])
def search_logs():
    """Search logs by message content"""
    logs = load_logs()
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400
    
    # Search in message field
    results = [log for log in logs if query in log.get('message', '').lower()]
    
    # Sort by timestamp
    results = sorted(results, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({
        "query": query,
        "total": len(results),
        "logs": results[:50]  # Limit to 50 results
    }), 200

@app.route('/logs/stats', methods=['GET'])
def get_stats():
    """Get logging statistics"""
    logs = load_logs()
    
    # Count by service
    service_counts = defaultdict(int)
    level_counts = defaultdict(int)
    
    for log in logs:
        service_counts[log.get('service', 'unknown')] += 1
        level_counts[log.get('level', 'unknown')] += 1
    
    return jsonify({
        "total_logs": len(logs),
        "by_service": dict(service_counts),
        "by_level": dict(level_counts)
    }), 200

@app.route('/logs/anomaly', methods=['GET'])
def detect_anomaly():
    """Detect error spikes (anomaly detection)"""
    logs = load_logs()
    
    # Get logs from last 5 minutes
    five_min_ago = (datetime.now() - timedelta(minutes=5)).isoformat()
    recent_logs = [log for log in logs if log.get('timestamp', '') > five_min_ago]
    
    if not recent_logs:
        return jsonify({
            "anomaly_detected": False,
            "message": "No recent logs"
        }), 200
    
    # Calculate error rate
    error_logs = [log for log in recent_logs if log.get('level') == 'ERROR']
    error_rate = (len(error_logs) / len(recent_logs)) * 100
    
    # Threshold: 5% error rate
    threshold = 5.0
    anomaly_detected = error_rate > threshold
    
    return jsonify({
        "anomaly_detected": anomaly_detected,
        "error_rate": round(error_rate, 2),
        "threshold": threshold,
        "total_logs": len(recent_logs),
        "error_logs": len(error_logs),
        "message": f"⚠️ ALERT: Error rate is {error_rate:.2f}%" if anomaly_detected else "System normal"
    }), 200

@app.route('/logs/trace/<correlation_id>', methods=['GET'])
def trace_request(correlation_id):
    """Trace a request across all services"""
    logs = load_logs()
    
    # Find all logs with this correlation ID
    trace_logs = [log for log in logs if log.get('correlation_id') == correlation_id]
    
    if not trace_logs:
        return jsonify({"error": "No logs found for this correlation ID"}), 404
    
    # Sort by timestamp
    trace_logs = sorted(trace_logs, key=lambda x: x.get('timestamp', ''))
    
    # Build journey
    journey = []
    for log in trace_logs:
        journey.append({
            "timestamp": log.get('timestamp'),
            "service": log.get('service'),
            "level": log.get('level'),
            "message": log.get('message')
        })
    
    return jsonify({
        "correlation_id": correlation_id,
        "total_steps": len(journey),
        "journey": journey
    }), 200

@app.route('/logs/clear', methods=['DELETE'])
def clear_logs():
    """Clear all logs (for testing)"""
    save_logs([])
    return jsonify({"message": "All logs cleared"}), 200

if __name__ == '__main__':
    print("🚀 Log Collector starting on port 5000...")
    print("📊 Logs will be stored in logs_database.json")
    app.run(debug=True, port=5000)