# CloudNativeShop

CloudNativeShop is a production-oriented cloud-native e-commerce platform
built to practice modern DevOps, DevSecOps, Kubernetes, GitOps,
observability, and AWS cloud engineering.

## Current Architecture

- Product Service - FastAPI
- Order Service - FastAPI
- PostgreSQL - planned
- Docker - planned
- Kubernetes - planned
- Jenkins CI/CD - planned
- SonarQube - planned
- Trivy - planned
- Helm - planned
- Argo CD - planned
- Prometheus - planned
- Grafana - planned
- Loki - planned
- Terraform - planned
- AWS EKS - planned

## Services

### Product Service

Port: `8001`

Endpoints:

- `GET /`
- `GET /health`
- `GET /products`
- `GET /products/{product_id}`

### Order Service

Port: `8002`

Endpoints:

- `GET /`
- `GET /health`
- `GET /orders`
- `GET /orders/{order_id}`

## Goal

Build and deploy the platform using an end-to-end
DevSecOps and GitOps workflow.