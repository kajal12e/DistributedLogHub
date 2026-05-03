import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log_collector.app import app, save_logs, load_logs

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear logs before each test
        save_logs([])
        yield client

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_collect_log(client):
    """Test log collection"""
    log_data = {
        "service": "test_service",
        "level": "INFO",
        "message": "Test message",
        "correlation_id": "test-123",
        "timestamp": "2024-01-01T12:00:00"
    }
    
    response = client.post('/logs', json=log_data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'log_id' in data

def test_get_logs(client):
    """Test log retrieval"""
    # First, add some logs
    for i in range(3):
        client.post('/logs', json={
            "service": f"service_{i}",
            "level": "INFO",
            "message": f"Message {i}",
            "correlation_id": f"corr-{i}",
            "timestamp": "2024-01-01T12:00:00"
        })
    
    # Retrieve logs
    response = client.get('/logs')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 3

def test_filter_by_service(client):
    """Test filtering logs by service"""
    # Add logs from different services
    client.post('/logs', json={
        "service": "user_service",
        "level": "INFO",
        "message": "User log",
        "correlation_id": "c1",
        "timestamp": "2024-01-01T12:00:00"
    })
    client.post('/logs', json={
        "service": "order_service",
        "level": "INFO",
        "message": "Order log",
        "correlation_id": "c2",
        "timestamp": "2024-01-01T12:00:00"
    })
    
    # Filter by user_service
    response = client.get('/logs?service=user_service')
    data = response.get_json()
    assert data['total'] == 1
    assert data['logs'][0]['service'] == 'user_service'

def test_filter_by_level(client):
    """Test filtering logs by level"""
    # Add logs with different levels
    client.post('/logs', json={
        "service": "test",
        "level": "ERROR",
        "message": "Error occurred",
        "correlation_id": "c1",
        "timestamp": "2024-01-01T12:00:00"
    })
    client.post('/logs', json={
        "service": "test",
        "level": "INFO",
        "message": "Info message",
        "correlation_id": "c2",
        "timestamp": "2024-01-01T12:00:00"
    })
    
    # Filter by ERROR
    response = client.get('/logs?level=ERROR')
    data = response.get_json()
    assert data['total'] == 1
    assert data['logs'][0]['level'] == 'ERROR'

def test_correlation_trace(client):
    """Test correlation ID tracking"""
    correlation_id = "trace-test-123"
    
    # Add multiple logs with same correlation ID
    services = ['user_service', 'order_service', 'product_service']
    for service in services:
        client.post('/logs', json={
            "service": service,
            "level": "INFO",
            "message": f"Processing in {service}",
            "correlation_id": correlation_id,
            "timestamp": "2024-01-01T12:00:00"
        })
    
    # Trace the request
    response = client.get(f'/logs/trace/{correlation_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_steps'] == 3
    assert len(data['journey']) == 3

def test_search_logs(client):
    """Test log search functionality"""
    # Add searchable logs
    client.post('/logs', json={
        "service": "test",
        "level": "INFO",
        "message": "User login successful",
        "correlation_id": "c1",
        "timestamp": "2024-01-01T12:00:00"
    })
    client.post('/logs', json={
        "service": "test",
        "level": "INFO",
        "message": "Order created",
        "correlation_id": "c2",
        "timestamp": "2024-01-01T12:00:00"
    })
    
    # Search for "login"
    response = client.get('/logs/search?q=login')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 1
    assert 'login' in data['logs'][0]['message'].lower()

def test_stats(client):
    """Test statistics endpoint"""
    # Add diverse logs
    client.post('/logs', json={
        "service": "user_service",
        "level": "INFO",
        "message": "Test",
        "correlation_id": "c1",
        "timestamp": "2024-01-01T12:00:00"
    })
    client.post('/logs', json={
        "service": "user_service",
        "level": "ERROR",
        "message": "Test",
        "correlation_id": "c2",
        "timestamp": "2024-01-01T12:00:00"
    })
    client.post('/logs', json={
        "service": "order_service",
        "level": "INFO",
        "message": "Test",
        "correlation_id": "c3",
        "timestamp": "2024-01-01T12:00:00"
    })
    
    response = client.get('/logs/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_logs'] == 3
    assert 'user_service' in data['by_service']
    assert 'INFO' in data['by_level']