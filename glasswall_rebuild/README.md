# Glasswall Rebuild Service

### Usage

`docker build -t glasswall-rebuild .`

`docker-compose up`

### Endpoints 

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/process` | Send malicious file and get cleaned file   | `{"file": "<raw file>"}` |	

