from fastapi import FastAPI, HTTPException
import boto3
from botocore.exceptions import ClientError, BotoCoreError
import os
import logging

# -------------------------------------
# Config
# -------------------------------------
app = FastAPI(title="AWS S3 Replicator")

# Ensure folder exists
TARGET_DIR = os.environ.get("TARGET_DIR", "replicated_files")
os.makedirs(TARGET_DIR, exist_ok=True)

# Create S3 client using environment credentials
s3 = boto3.client("s3")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------
# Endpoints
# -------------------------------------
@app.post("/v1/replicate")
async def replicate_file(body: dict):
    """
    Download a file from S3 and save locally.
    Body JSON: { "s3_bucket": "bucket-name", "s3_key": "path/to/file.csv" }
    """
    s3_bucket = body.get("s3_bucket")
    s3_key = body.get("s3_key")

    if not s3_bucket or not s3_key:
        raise HTTPException(status_code=400, detail="s3_bucket and s3_key are required")

    file_name = os.path.basename(s3_key)
    target_path = os.path.join(TARGET_DIR, file_name)

    # Idempotency check
    if os.path.exists(target_path):
        logging.info(f"File already exists locally: {target_path}")
        return {"status": "already_exists", "file": target_path}

    try:
        logging.info(f"Downloading s3://{s3_bucket}/{s3_key} → {target_path}")
        s3.download_file(s3_bucket, s3_key, target_path)
        logging.info("Download complete")
        return {"status": "replicated", "file": target_path}
    except (ClientError, BotoCoreError) as e:
        logging.error(f"S3 download failed: {e}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
