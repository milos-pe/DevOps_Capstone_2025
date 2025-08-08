# Book Catalog API

A DevOps capstone project implementing a Django REST API for managing book collections. \
The project includes automated testing, Docker containerization, and Kubernetes deployment using Helm charts, with CI/CD via GitHub Actions.

## Project Architecture
- **RESTful API** built with Django REST Framework to manage a book catalog and expose HTTP endpoints for CRUD operations.
- **PostgreSQL** as the database backend for storing book information.
- **Docker** for packaging the Django app and its dependencies into containers.
- **Kubernetes** to manage and scale containerized applications automatically.
- **Helm** packages the application into a single chart for easier deployment and management.
- **GitHub Actions** to automate testing, Docker builds, versioning, and Helm updates.
- **ArgoCD** for automatically deploying updates to the Kubernetes cluster.

## Installation Guide

Follow the steps below to set up and run the Book Catalog API locally or on a Kubernetes cluster.

### Prerequisites
- **Python:** for local development and testing (Python 3.12 used)
- **Docker:** for building and running containers
- **k3d:** to create a local Kubernetes cluster using Docker
- **kubectl:** Kubernetes command-line interface
- **Helm 3:** for deploying Helm charts to Kubernetes
- **Git:** to clone the repository

### Steps

**1. Clone the repository**
```bash
$ git clone git@github.com:milos-pe/DevOps_Capstone_2025.git
$ cd devops_capstone_2025
```

**2. Start the application locally with Docker Compose**
```bash
$ docker compose up --build
```

**3. Create a Kubernetes cluster using k3d**
```bash
$ k3d cluster create devops-capstone \
    --port "8081:80@loadbalancer" \
    --port "8443:443@loadbalancer" \
    --port "30000-30010:30000-30010@server:0"
```

**4. Deploy the PostgreSQL database to Kubernetes using Bitnami Helm chart with custom values**
```bash
$ helm install books-database oci://registry-1.docker.io/bitnamicharts/postgresql -f postgres-helm/values.yml
```

**5. Deploy the Django application to Kubernetes**
```bash
$ helm install books ./bookcatalog-chart
```

**6. Verify the Deployment**
```bash
$ kubectl get pods
$ kubectl get svc
$ kubectl get ingress
```

**7. Deploy ArgoCD to the Kubernetes using the ArgoCD Helm chart with custom values**
```bash
$ helm repo add argo https://argoproj.github.io/argo-helm
$ helm repo update
$ kubectl create namespace argocd
$ helm -n argocd install argocd argo/argo-cd -f argo-helm/values.yaml
```

## API Endpoints
| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/api/health`     | Health check      |
| POST   | `/api/books/`     | Create a new book |
| GET    | `/api/books/`     | List all books    |
| GET    | `/api/book/<id>/` | Retrieve a book   |
| PUT    | `/api/book/<id>/` | Update a book     |
| DELETE | `/api/book/<id>/` | Delete a book     |

### GET /api/health
Check whether the API is up and running.
```bash
curl -X GET http://localhost:8081/api/health
# Response:
# { "status": "ok" }
```

### POST /api/books/
Create a new book.
```bash
curl -X POST http://localhost:8081/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for APIs",
    "description": "Practical guide to building web APIs",
    "author": "William Vincent",
    "isbn": "9781735467207",
    "published_date": "2022-01-01"
  }'

# Response (HTTP 201):
# {
#   "title": "Django for APIs",
#   "description": "Practical guide to building web APIs",
#   "author": "William Vincent",
#   "isbn": "9781735467207",
#   "published_date": "2022-01-01",
#   "created_at": "2025-07-30T10:15:56.347755Z"
# }
```

### GET /api/books/
List all the books.
```bash
curl -X GET http://localhost:8081/api/books/
# Response (HTTP 200):
# {
#   "title": "Django for APIs",
#   "description": "Practical guide to building web APIs",
#   "author": "William Vincent",
#   "isbn": "9781735467207",
#   "published_date": "2022-01-01",
#   "created_at": "2025-07-30T10:15:56.347755Z"
# }
```

### GET /api/book/<id>/
Fetch the book with specified ID.
```bash
curl -X GET http://localhost:8081/api/book/1/
# Response (HTTP 200):
# {
#   "title": "Django for APIs",
#   "description": "Practical guide to building web APIs",
#   "author": "William Vincent",
#   "isbn": "9781735467207",
#   "published_date": "2022-01-01",
#   "created_at": "2025-07-30T10:15:56.347755Z"
# }
```

### PUT /api/book/<id>/
Update the book with specified ID.
```bash
curl -X PUT http://localhost:8081/api/book/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for APIs v2",
    "description": "Practical guide to building web APIs",
    "author": "William Vincent",
    "isbn": "9781735467207",
    "published_date": "2022-01-01"
  }'

# Response (HTTP 202):
# {
#   "title": "Django for APIs v2",
#   "description": "Practical guide to building web APIs",
#   "author": "William Vincent",
#   "isbn": "9781735467207",
#   "published_date": "2022-01-01",
#   "created_at": "2025-07-30T10:15:56.347755Z"
# }
```

### DELETE /api/book/<id>/
Delete the book with specified ID.
```bash
curl -X DELETE http://localhost:8081/api/book/1/
# Response (HTTP 204): no content
```

## CI/CD Pipeline
- test &rarr; Runs unit test to validate API endpoints.
- runmigrations &rarr; Applies database migrations to ensure the schema is up to date.
- migration‑check &rarr; Verifies that there are no unapplied migrations.
- semantic‑release &rarr; Generates a version number and changelog based on commit messages and publishes a release.
- build‑docker‑image &rarr; Builds the Docker image and pushes it to GitHub Container Registry (GHCR).
- deploy‑application &rarr; Updates the `environments/production/values.yaml` tag in GitHub repository.

## Technologies Used
- Python 3.12
- Django & Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- GitHub Actions
- Kubernetes & Helm
- Bitnami PostgreSQL chart
- ArgoCD image

## Author
Milos Petrovic  
DevOps Diploma – CCT College Dublin, 2025