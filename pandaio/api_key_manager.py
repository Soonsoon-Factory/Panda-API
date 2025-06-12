from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pandaio.models import SessionLocal, APIKey
from datetime import datetime, timedelta
import secrets

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_api_key():
    """64자 길이의 랜덤 API Key 생성"""
    return secrets.token_urlsafe(64)

@router.post("/generate-api-key/")
def create_api_key(expiration_days: int = 30, db: Session = Depends(get_db)):
    """
    API Key 발급 엔드포인트
    - expiration_days: 만료일 설정 (기본값: 30일)
    """
    api_key = generate_api_key()
    expires_at = datetime.utcnow() + timedelta(days=expiration_days)

    new_key = APIKey(
        key=api_key,
        is_active=True,
        created_at=datetime.utcnow(),
        expires_at=expires_at
    )

    db.add(new_key)
    db.commit()

    return {
        "api_key": api_key,
        "expires_at": expires_at
    }
