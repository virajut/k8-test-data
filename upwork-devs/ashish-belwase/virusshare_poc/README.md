# VirusShare POC

### Usage

`python src/`

### Endpoints

| Endpoint | Description             | Payload     |
| -------- | ------------------------| ----------- |
| `/scrape-vs-file`  | Download a file from VS   | `{"api_key": "","hash"   : ""}` |
| `/check-malicious` | Check if a file is malicious   | `{"file": "<binary file>"}` |