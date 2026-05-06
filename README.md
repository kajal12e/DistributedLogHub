# DistributedLogHub - Microservices Log Aggregation System

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://log-collector-kajal.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-black)](https://flask.palletsprojects.com/)
[![Render](https://img.shields.io/badge/Deployed-Render-46E3B7)](https://render.com/)

> **🚀 Live Demo:** [Log Collector API](https://log-collector-kajal.onrender.com/)

**Production-grade distributed logging framework for microservices with centralized aggregation, correlation ID tracing, and real-time observability.**

---

### **Live Services - Click to Test**
| Service | Live URL | Status |
| --- | --- | --- |
| **Log Collector** | https://log-collector-kajal.onrender.com/ | Central API storing all logs |
| **User Service** | https://user-service-kajal.onrender.com/ | Handles user operations |
| **Order Service** | https://order-service-kajal.onrender.com/ | Handles order operations |
| **Product Service** | https://product-service-kajal.onrender.com/ | Handles product operations |

> **Note:** Render free tier spins down after 15 min inactivity. First request takes ~50s to wake up. If you see "Application unavailable", refresh after 1 min.

---

## **Architecture**

┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ User Service  │────→│               │←────│ Order Service │
└───────────────┘     │ Log Collector │     └───────────────┘
                      │     API       │
┌───────────────┐     │               │     ┌───────────────┐
│Product Service│────→│  /logs POST   │←────│   External    │
└───────────────┘     └───────────────┘     └───────────────┘
All microservices send structured logs via `LOG_COLLECTOR_URL` environment variable. Each request gets a `correlation_id` to trace it across services.

## **Tech Stack**
`Python 3.11` `Flask` `Gunicorn` `REST APIs` `Microservices` `Render Cloud` `Docker` `Environment Variables` `Distributed Tracing`

## **Key Features**
1. **Centralized Logging** - Single API aggregates logs from all microservices
2. **Correlation IDs** - Track a request across user → order → product services  
3. **Environment-Based Config** - `LOG_COLLECTOR_URL` injected via Render env vars
4. **Fault Tolerant** - Services don't crash if log-collector is down
5. **Production Ready** - Gunicorn WSGI server, health checks, proper status codes

## **Quick Test - Prove It's Working**

**1. Wake up the services** - Open all 4 live URLs above and wait for JSON response

**2. Send a test request to user-service:**
```bash
curl -X POST https://user-service-kajal.onrender.com/users \
-H "Content-Type: application/json" \
-d "{\"name\":\"Kajal\",\"email\":\"test@example.com\"}"


*3. Check the logs:* Open https://log-collector-kajal.onrender.com/logs

*4. Result:* You'll see a new log entry with `"service": "user-service"` and a unique `correlation_id`. This proves distributed logging works.

## *Local Development*
git clone https://github.com/kajal12e/DistributedLogHub.git
cd DistributedLogHub
pip install -r requirements.txt
docker-compose up  # Runs all 4 services locally


## *🎥 Demo Video*
*[Watch 60-sec live demo](your-video-link-here)* - Shows real-time log flow from user-service → log-collector

---

*Built by Kajal* |[LinkedIn](https://www.linkedin.com/in/kajal-kumari-58208b252) | Deployed on Render | Microservices + Observability
