To run Dockerfile:
```
docker build -f src/deployment/Dockerfile -t myapp .
```
then 
```
docker run -p 8000:8000 myapp
```