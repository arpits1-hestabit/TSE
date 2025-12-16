# HTTPS / SSL Setup — Day-4 reverse-proxy (nginx)

1. Install mkcert and register a local CA (one-time):
```bash
sudo apt install mkcert libnss3-tools
mkcert -install
```

2. Generate certs for localhost :
```bash
mkdir -p ./Day-4/nginx/ssl
cd ./Day-4/nginx/ssl
mkcert certnew
```
---

## NGINX config 

Ensure nginx.conf points to the cert/key paths inside the container:
```
ssl_certificate     /etc/nginx/ssl/certnew.pem;
ssl_certificate_key /etc/nginx/ssl/certnew-key.pem;
```
---

## Docker Compose 

```
services:
  nginx:
    image: nginx:stable
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/ssl:ro 
    ports:
      - "80:80"
      - "443:443"
```

---

## Run & verify

1. Start stack:
```bash
docker compose up -d --build
```

2. Verify containers:
```bash
docker ps
```

---

## Summary

- For local development: mkcert -> mount certs to `./Day-4/nginx/ssl` -> docker compose up.

- Also remember to add the certs. in hosts -
```
sudo nano /etc/hosts
```


## Screenshots

![alt text](/Week-5/Day-4/Attachments/image.png)

![alt text](/Week-5/Day-4/Attachments/image-1.png)

![alt text](/Week-5/Day-4/Attachments/image-2.png)