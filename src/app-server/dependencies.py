from fastapi import Depends
from typing import Annotated
from service.upbit_service import UpbitService


# 의존성 주입 함수들
def get_upbit_service() -> UpbitService:
    return UpbitService()
