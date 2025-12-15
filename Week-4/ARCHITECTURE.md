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

