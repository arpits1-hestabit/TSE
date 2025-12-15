# Production Deployment Guide

## Overview
The application is deployed in production using **PM2**, a robust process manager for Node.js. PM2 ensures reliability through process monitoring, automatic restarts, clustering, and zero-downtime reloads. All production-specific configuration is isolated inside the `prod/` directory.

---

## PM2 for Production
PM2 is well-suited for running applications in live environments.

**Key advantages:**
- Background process management
- Automatic restart on crashes
- Cluster mode for load balancing
- Centralized log handling
- Zero-downtime reloads

---

## Production Directory Structure
All production resources are kept separate from development code:

```
prod/
├── ecosystem.config.cjs # PM2 production configuration
└── src/
└── logs/ # Production logs
├── combined.log
└── requestlog.log
```
## Ecosystem Configuration
The `ecosystem.config.cjs` file defines how PM2 runs the application.

**Application settings:**
- Entry script: `../index.js`
- Watch mode: Disabled for stability
- Execution mode: `cluster`
- Instances: 5 worker processes

**Environment variables:**
- `PORT=3002`
- `MONGO_URI=<production MongoDB connection string>`

---

## Deployment Configuration
PM2’s deployment feature automates server updates.

**Deployment setup includes:**
- SSH user for server access
- Target host (server IP or hostname)
- Git branch: `origin/main`
- Git repository URL
- Deployment path on the server
- Post-deploy steps (install dependencies, reload PM2)

---

## Deployment Commands
Common production commands:

```bash
pm2 start prod/ecosystem.config.cjs
pm2 status
pm2 logs
pm2 reload ecosystem.config.cjs
pm2 stop ecosystem.config.cjs


