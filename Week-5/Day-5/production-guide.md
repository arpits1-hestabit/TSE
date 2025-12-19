# Production-Guide

## Overview of services
- server — Node API (server/)
- client — frontend (client/)
- nginx — TLS termination, reverse proxy and load balancing (nginx/)
- persistence — external managed DB
- certs — nginx/certs (week5.day5.pem, week5.day5-key.pem)

---

## Project Structure
```
├── deploy.sh
├── docker-compose.prod.yml
├── Attachments/
├── production-guide.md
├── package.json
├── client/
│   ├── .env
│   └── src/
│       ├── App.css
│       ├── App.jsx
│       ├── global.css
│       ├── index.css
│       ├── main.jsx
│       └── assets/
├── nginx/
│   ├── nginx.conf
│   └── certs/
│       ├── week5.day5-key.pem
│       └── week5.day5.pem
└── server/
    ├── .env
    ├── .gitignore
    ├── Dockerfile
    ├── index.js
    ├── package.json

```
---


## TLS certificates
- Place cert files in `nginx/certs/` or mount host certificate directory into container (read-only).
- Ensure nginx.conf refers to mounted cert paths:
  - ssl_certificate /etc/nginx/ssl/week5.day5.pem;
  - ssl_certificate_key /etc/nginx/ssl/week5.day5-key.pem;

---

## Using deploy.sh

```
chmod +x deploy.sh
./deploy.sh
```
---

## Health check route
Add to backend in index.js:

```
app.get("/health", (req, res) => res.send("OK"));
```

This endpoint is used by Docker healthchecks and monitoring.



## Screenshots

 1. Running Container -
![alt text](/Week-5/Day-5/Attachments/image-2.png)

 2. Running app -
![alt text](/Week-5/Day-5/Attachments/image-3.png)

 3. Database Entries -
![alt text](/Week-5/Day-5/Attachments/image-4.png)

4. Volumes -
![alt text](/Week-5/Day-5/Attachments/image-1.png)

5. Health Check - 
![alt text](/Week-5/Day-5/Attachments/image.png)
