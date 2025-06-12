from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from pandaio.models import SessionLocal, APIKey
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_api_key(api_key: str = Header(..., alias="api-key"), db: Session = Depends(get_db)):
    """
    API Key 인증 모듈
    """
    key_record = db.query(APIKey).filter(APIKey.key == api_key).first()

    if not key_record:
        raise HTTPException(status_code=403, detail="Invalid or inactive API Key")

    if not key_record.is_active:
        raise HTTPException(status_code=403, detail="API Key is inactive")

    if key_record.expires_at and key_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="API Key has expired")

    return api_key
