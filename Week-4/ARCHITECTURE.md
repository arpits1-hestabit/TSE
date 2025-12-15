# Architecture Overview — Week-4 Project

## Project layout -
```
src/
├── config/          # Environment configuration and setup
├── controllers/     # Request/response handling, HTTP layer
├── services/        # Business logic and orchestration
├── repositories/    # Data access layer, database operations
├── models/          # Database schemas and Mongoose models
├── routes/          # API endpoint definitions and routing
├── middlewares/     # Request processing (validation, security, tracing)
├── validations/     # Input validation schemas (Joi)
├── jobs/            # Background job queues and workers
├── loaders/         # Application initialization modules
├── utils/           # Shared utilities (logging, helpers)
└── docs/            # API documentation (Swagger)

```

## High-level flow (diagram)

```mermaid
flowchart LR
  Client[Client / Browser / Mobile] --> LB[Load Balancer / Reverse Proxy]
  LB --> PM2[PM2 / Process Manager]
  PM2 --> App[Node App (index.js)]
  App --> Loaders[src/loaders]
  Loaders --> Express[Express Initialization]
  Express --> Middlewares[src/middlewares]
  Express --> Routes[src/routes]
  Routes --> Controllers[src/controllers]
  Controllers --> Services[src/services]
  Services --> Repositories[src/repositories]
  Repositories --> Models[src/models (DB)]
  Services --> Jobs[src/jobs & queues]
  Jobs --> Workers[Workers (background)]
  Services --> External[External APIs / Providers]
  App --> Utils[src/utils & logging]
  App --> Docs[src/docs (Swagger)]
```
