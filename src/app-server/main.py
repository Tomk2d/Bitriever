from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# API 라우터들 import
from api.upbit_fetch_api import router as fetch_router

app = FastAPI(
    title="BIT Diary API", description="암호화폐 투자 지원을 위한 API", version="0.1.1"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(fetch_router, prefix="/api", tags=["fetch"])


@app.get("/")
async def root():
    return {"message": "BIT Diary API", "version": "0.1.1"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
