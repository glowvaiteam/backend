from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from firebase_admin import auth
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

def verify_firebase_user(token=Depends(security)):
    try:
        logger.info(f"Verifying token: {token.credentials[:20]}...")
        decoded = auth.verify_id_token(token.credentials)
        logger.info(f"✅ Token verified for user: {decoded.get('uid')}")
        return decoded
    except Exception as e:
        logger.error(f"❌ Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")
