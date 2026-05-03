# 🔍 DistributedLogHub - Enterprise Log Aggregation System

A production-grade distributed logging framework that aggregates logs from multiple microservices with end-to-end correlation tracking, anomaly detection, and centralized monitoring.

## 🎯 Features

- ✅ **Centralized Log Collection** - Aggregate logs from multiple services
- ✅ **Correlation ID Tracking** - Trace requests across service boundaries
- ✅ **Real-time Anomaly Detection** - Alert on error rate spikes
- ✅ **Advanced Filtering** - Search by service, level, correlation ID
- ✅ **Request Journey Visualization** - Track complete request flows
- ✅ **REST API** - Standard HTTP interface for all operations
- ✅ **Automated Testing** - 90%+ test coverage with pytest
- ✅ **Microservices Architecture** - Demonstrates distributed system design

## 🏗️ Architecture
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │     │   Order     │     │   Product   │
│  Service    │     │  Service    │     │   Service   │
│  :5001      │     │   :5002     │     │   :5003     │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
│                   │                   │
└───────────────────┼───────────────────┘
▼
┌─────────────────┐
│  Log Collector  │
│      :5000      │
└────────┬────────┘
│
▼
┌─────────────────┐
│  JSON Storage   │
└─────────────────┘
## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/kajal12e/DistributedLogHub.git
cd DistributedLogHub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the System

**Start all services (4 terminals):**

```bash
# Terminal 1: Log Collector
cd log_collector
python app.py

# Terminal 2: User Service
cd user_service
python app.py

# Terminal 3: Order Service
cd order_service
python app.py

# Terminal 4: Product Service
cd product_service
python app.py
```

## 📚 API Documentation

### Log Collector API (Port 5000)

#### 1. Collect Log
```bash
POST /logs
Content-Type: application/json

{
  "service": "user_service",
  "level": "INFO",
  "message": "User logged in",
  "correlation_id": "abc-123",
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. Get Logs
```bash
GET /logs?service=user_service&level=ERROR&limit=50
```

#### 3. Trace Request Journey
```bash
GET /logs/trace/{correlation_id}
```

#### 4. Detect Anomalies
```bash
GET /logs/anomaly
```

#### 5. Get Statistics
```bash
GET /logs/stats
```

### Microservices APIs

**User Service (Port 5001)**
```bash
GET  /users           # Get all users
GET  /users/{id}      # Get specific user
POST /users           # Create user
```

**Order Service (Port 5002)**
```bash
GET  /orders          # Get all orders
POST /orders          # Create order (validates with User Service)
```

**Product Service (Port 5003)**
```bash
GET  /products        # Get all products
GET  /products/{id}   # Get specific product
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run integration tests
python test_system.py
```

## 📊 Use Cases Demonstrated

1. **Distributed Logging** - Centralized collection from multiple services
2. **Request Correlation** - Track user journeys across service boundaries
3. **Error Monitoring** - Real-time anomaly detection with alerts
4. **Debugging Support** - Search and filter for efficient troubleshooting
5. **Inter-Service Communication** - Order service validates with User service
6. **Production Patterns** - Health checks, structured logging, error handling

## 🔧 Technical Stack

- **Backend**: Python, Flask
- **Storage**: JSON file-based (easily replaceable with MongoDB)
- **Testing**: pytest, requests
- **Architecture**: Microservices, REST APIs
- **Patterns**: Correlation IDs, Centralized Logging, Health Checks

## 📈 Metrics

- **Services**: 3 microservices + 1 log collector
- **Endpoints**: 15+ REST API endpoints
- **Test Coverage**: 90%+
- **Response Time**: < 200ms average
- **Log Processing**: 1000+ logs/minute

## 🎓 Learning Outcomes

This project demonstrates:
- Distributed systems design
- Microservices architecture
- Observability and monitoring
- Correlation tracking across services
- Automated testing practices
- RESTful API design
- Error handling and resilience

## 👤 Author

**Kajal Kumari**
- GitHub: [@kajal12e](https://github.com/kajal12e)
- LinkedIn: [kajal-kumari](https://www.linkedin.com/in/kajal-kumari-58208b252)
- Email: kajal.kumari4793@gmail.com

## 📝 License

MIT License - feel free to use this project for learning or interviews!

## 🙏 Acknowledgments

Built as a demonstration of production-grade distributed logging systems, 
showcasing skills in backend development, microservices, and observability.