# Customer Support Ticketing System

A microservices-based customer support ticketing platform built with FastAPI, Docker, Docker Compose, and Kubernetes.

---

## Architecture

The system is organized into 4 independent microservices that communicate with each other through HTTP APIs:

| Service | Port | Responsibility |
|---|---|---|
| Ticket Service | 8000 | Create, update, and track tickets |
| Support Service | 8001 | Assign, respond, and resolve tickets |
| Notification Service | 8002 | Send alerts on ticket status changes |
| Reporting Service | 8003 | Generate reports on tickets and responses |

### Service Communication

```
support-service     → ticket-service       (update ticket status)
support-service     → notification-service (send alerts)
reporting-service   → ticket-service       (get all tickets)
reporting-service   → support-service      (get all responses)
```

---

## Project Structure

```
ticketing-system/
├── ticket-service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── support-service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── notification-service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── reporting-service/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/
│   ├── ticket-service-deployment.yaml
│   ├── ticket-service-service.yaml
│   ├── support-service-deployment.yaml
│   ├── support-service-service.yaml
│   ├── notification-service-deployment.yaml
│   ├── notification-service-service.yaml
│   ├── reporting-service-deployment.yaml
│   └── reporting-service-service.yaml
├── docker-compose.yml
├── run-env
├── run-k8s-env
└── README.md
```

---

## API Endpoints

### Ticket Service (port 8000)
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| POST | /tickets | Create a new ticket |
| GET | /tickets | Get all tickets |
| GET | /tickets/{id} | Get ticket by ID |
| PUT | /tickets/{id} | Update ticket status |

### Support Service (port 8001)
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| POST | /assign | Assign ticket to an agent |
| GET | /assignments | Get all assignments |
| POST | /respond | Respond to a ticket |
| GET | /responses | Get all responses |
| POST | /resolve | Resolve a ticket |
| GET | /resolved | Get all resolved tickets |
| GET | /tickets | Get all tickets from ticket-service |

### Notification Service (port 8002)
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| POST | /notify | Create a new notification |
| GET | /notifications | Get all notifications |

### Reporting Service (port 8003)
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| GET | /report | Generate full system report |

---

## Ticket Status Flow

```
Customer creates ticket  →  open
Agent assigns ticket     →  in-progress
Agent responds           →  in-progress
Agent resolves ticket    →  resolved
```

---

## Running the Project

### Option 1 — Docker Compose (Local Development)

```bash
# Build and start all services
docker compose up --build

# Access services
# http://localhost:8000/docs  → ticket-service
# http://localhost:8001/docs  → support-service
# http://localhost:8002/docs  → notification-service
# http://localhost:8003/docs  → reporting-service
```

### Option 2 — Kubernetes (Production)

**Prerequisites:**
- Docker
- kubectl
- Minikube

**Setup:**

```bash
# Start Minikube
minikube start --driver=docker

# Point terminal to Minikube's Docker environment
eval $(minikube docker-env)

# Build all images inside Minikube
docker build -t ticket-service ./ticket-service
docker build -t support-service ./support-service
docker build -t notification-service ./notification-service
docker build -t reporting-service ./reporting-service

# Deploy all services
bash run-k8s-env
```

**Access services:**
```
http://<minikube-ip>:30000/docs  → ticket-service
http://<minikube-ip>:30001/docs  → support-service
http://<minikube-ip>:30002/docs  → notification-service
http://<minikube-ip>:30003/docs  → reporting-service
```

Get your Minikube IP with:
```bash
minikube ip
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| httpx | Inter-service HTTP communication |
| Docker | Containerization |
| Docker Compose | Local orchestration |
| Kubernetes | Production orchestration |
| Minikube | Local Kubernetes cluster |