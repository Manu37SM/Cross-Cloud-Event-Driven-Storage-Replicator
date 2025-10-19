
# Assignment 1 - Cross-Cloud Event-Driven Storage Replicator (Minimal)
This is a minimal FastAPI service exposing POST /v1/replicate.

Run (locally):

1. Create virtual environment using below commands
   `python -m venv venv`
   `venv\Scripts\activate`
2. Install deps: `pip install -r requirements.txt`
3. Set env variables for AWS and GCP credentials.
4. Start: `uvicorn app:app --reload --port 8001`
5. Example request:
   `curl -X POST http://localhost:8001/v1/replicate -H 'Content-Type: application/json' -d '{"s3_bucket":"my-bucket","s3_key":"path/to/file.csv"}'`