from fastapi import FastAPI
from pandaio.api_key_manager import router as api_key_router
from pandaio.routes.api_router import router as api_router


app = FastAPI()

# API Key 발급 엔드포인트 등록
app.include_router(api_key_router, prefix="/auth", tags=["Authentication"])

# /api 경로로 라우터 등록
app.include_router(api_router, prefix="/api", tags=["AI"])

# 로컬 테스트용 uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# 배포용
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("pandaio.main:app", host="0.0.0.0", port=8000, reload=True)
