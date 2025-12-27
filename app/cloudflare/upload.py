# app/cloudflare/upload.py

import boto3
import uuid
import os
from dotenv import load_dotenv

# ✅ LOAD .env FILE
load_dotenv()

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")

# ✅ SAFETY CHECK (VERY IMPORTANT)
if not all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET, R2_PUBLIC_URL]):
    raise RuntimeError("Missing one or more Cloudflare R2 environment variables")

s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
)

def upload_image_to_cloudflare(image_bytes: bytes, content_type: str) -> str:
    filename = f"faces/{uuid.uuid4()}.jpg"

    s3.put_object(
        Bucket=R2_BUCKET,          # ✅ STRING
        Key=filename,
        Body=image_bytes,
        ContentType=content_type,
    )

    # ✅ PUBLIC URL FOR FRONTEND / ML
    return f"{R2_PUBLIC_URL}/{filename}"
