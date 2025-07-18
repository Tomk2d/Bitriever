from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import importlib

app = FastAPI(
    title="BIT Diary API", description="암호화폐 투자 지원을 위한 API", version="0.1.1"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 자동 라우터 등록 함수
def register_routers():
    api_dir = "api"

    # api 디렉토리의 모든 파일을 스캔
    for filename in os.listdir(api_dir):
        if filename.endswith("_api.py"):
            module_name = filename[:-3]
            module_path = f"{api_dir}.{module_name}"

            try:
                module = importlib.import_module(module_path)

                # router 속성이 있는지 확인
                if hasattr(module, "router"):
                    router = getattr(module, "router")
                    tag = module_name.replace("_api", "").title()

                    # 라우터 등록
                    app.include_router(router, prefix="/api", tags=[tag])
                    print(f"라우터 등록됨: {module_name}")

            except Exception as e:
                print(f"라우터 등록 실패: {module_name}, 에러: {e}")


# 자동 라우터 등록 실행
register_routers()


@app.get("/")
async def root():
    return {"message": "BIT Diary API", "version": "0.1.1"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
