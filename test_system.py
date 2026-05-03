import requests
import time

BASE_URLS = {
    'log_collector': 'http://localhost:5000',
    'user_service': 'http://localhost:5001',
    'order_service': 'http://localhost:5002',
    'product_service': 'http://localhost:5003'
}

def test_health_checks():
    """Test all services are running"""
    print("\n🏥 Testing Health Checks...")
    for service, url in BASE_URLS.items():
        try:
            response = requests.get(f"{url}/health")
            print(f"✅ {service}: {response.json()}")
        except Exception as e:
            print(f"❌ {service}: {e}")

def test_user_operations():
    """Test user service and log generation"""
    print("\n👤 Testing User Service...")
    
    # Get all users
    response = requests.get(f"{BASE_URLS['user_service']}/users")
    data = response.json()
    print(f"✅ Found {len(data['users'])} users")
    print(f"   Correlation ID: {data['correlation_id']}")
    
    # Get specific user
    response = requests.get(f"{BASE_URLS['user_service']}/users/1")
    print(f"✅ User 1: {response.json()['user']['name']}")
    
    # Try to get non-existent user (generates error log)
    response = requests.get(f"{BASE_URLS['user_service']}/users/999")
    print(f"✅ Error test: {response.status_code} (expected 404)")

def test_order_creation():
    """Test order creation with inter-service communication"""
    print("\n🛒 Testing Order Creation...")
    
    order_data = {
        "user_id": 1,
        "product": "Laptop",
        "amount": 50000
    }
    
    response = requests.post(
        f"{BASE_URLS['order_service']}/orders",
        json=order_data
    )
    
    data = response.json()
    print(f"✅ Order created: ID {data['order']['id']}")
    print(f"   Correlation ID: {data['correlation_id']}")
    
    return data['correlation_id']

def test_log_retrieval():
    """Test log collector endpoints"""
    print("\n📋 Testing Log Retrieval...")
    
    # Get all logs
    response = requests.get(f"{BASE_URLS['log_collector']}/logs?limit=10")
    data = response.json()
    print(f"✅ Total logs: {data['total']}")
    
    # Get stats
    response = requests.get(f"{BASE_URLS['log_collector']}/logs/stats")
    stats = response.json()
    print(f"✅ Statistics:")
    print(f"   Total: {stats['total_logs']}")
    print(f"   By Service: {stats['by_service']}")
    print(f"   By Level: {stats['by_level']}")

def test_correlation_trace(correlation_id):
    """Test request tracing across services"""
    print(f"\n🔍 Testing Request Tracing...")
    print(f"   Correlation ID: {correlation_id}")
    
    response = requests.get(
        f"{BASE_URLS['log_collector']}/logs/trace/{correlation_id}"
    )
    
    data = response.json()
    print(f"✅ Journey found: {data['total_steps']} steps")
    for step in data['journey']:
        print(f"   → {step['service']}: {step['message']}")

def test_anomaly_detection():
    """Test anomaly detection"""
    print("\n⚠️  Testing Anomaly Detection...")
    
    # Generate some errors
    for i in range(5):
        requests.get(f"{BASE_URLS['user_service']}/users/999")
    
    time.sleep(1)
    
    response = requests.get(f"{BASE_URLS['log_collector']}/logs/anomaly")
    data = response.json()
    print(f"✅ Anomaly Status: {data['anomaly_detected']}")
    print(f"   Error Rate: {data['error_rate']}%")
    print(f"   Message: {data['message']}")

if __name__ == '__main__':
    print("="*50)
    print("🧪 DISTRIBUTED LOG SYSTEM - INTEGRATION TEST")
    print("="*50)
    
    test_health_checks()
    time.sleep(1)
    
    test_user_operations()
    time.sleep(1)
    
    correlation_id = test_order_creation()
    time.sleep(2)  # Wait for logs to be collected
    
    test_log_retrieval()
    time.sleep(1)
    
    test_correlation_trace(correlation_id)
    time.sleep(1)
    
    test_anomaly_detection()
    
    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETED!")
    print("="*50)