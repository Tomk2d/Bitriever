from fastapi import Depends
from typing import Annotated, Any
from repository.coin_repository import CoinRepository


# 싱글톤 인스턴스들
_upbit_service_instance = None
_coin_service_instance = None
_coin_repository_instance = None


# 의존성 주입 함수들
def get_upbit_service() -> Any:  # Any로 타입 힌트
    global _upbit_service_instance
    if _upbit_service_instance is None:
        from service.upbit_service import UpbitService  # lazy import

        _upbit_service_instance = UpbitService()
    return _upbit_service_instance


def get_coin_service() -> Any:  # Any로 타입 힌트
    global _coin_service_instance
    if _coin_service_instance is None:
        from service.coin_service import CoinService  # lazy import

        _coin_service_instance = CoinService()
    return _coin_service_instance


def get_coin_repository() -> CoinRepository:
    global _coin_repository_instance
    if _coin_repository_instance is None:
        _coin_repository_instance = CoinRepository()
    return _coin_repository_instance
