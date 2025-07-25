import os
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import logging
from typing import Annotated, Any
from fastapi import Depends
from dependencies import get_upbit_service, get_coin_service
from dto.http_response import ErrorResponse, SuccessResponse


router = APIRouter(prefix="/upbit")
load_dotenv()
logger = logging.getLogger(__name__)


@router.get("/allTradingHistory")
async def fetch_trading_history(
    upbit_service: Annotated[Any, Depends(get_upbit_service)]
):
    try:
        # 여기 나중에 db에서 조회하는걸로 변경
        access_key = os.getenv("UPBIT_ACCESS_KEY", "")
        secret_key = os.getenv("UPBIT_SECRET_KEY", "")

        uuids = upbit_service.fetch_all_trading_uuids(access_key, secret_key)

        trading_histies = upbit_service.fetch_all_trading_history(
            access_key, secret_key, uuids
        )
        return SuccessResponse(
            data=trading_histies, message="거래 내역 조회가 완료되었습니다"
        )
    except Exception as e:
        logger.error(f"예상치 못한 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                status_code=500,
                error_code="INTERNAL_SERVER_ERROR",
                message="서버 내부 오류가 발생했습니다",
                details=str(e),
            ).dict(),
        )


@router.post("/allCoinList")
async def fetch_and_save_all_coin_list(
    upbit_service: Annotated[Any, Depends(get_upbit_service)],
    coin_service: Annotated[Any, Depends(get_coin_service)],
):
    try:
        fetched_data_list = upbit_service.fetch_all_coin_list()
        saved_coin_list = coin_service.save_all_coin_list(fetched_data_list)

        return SuccessResponse(
            data=saved_coin_list, message="모든 코인 리스트 조회가 완료되었습니다"
        )
    except Exception as e:
        logger.error(f"예상치 못한 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                status_code=500,
                error_code="INTERNAL_SERVER_ERROR",
                message="서버 내부 오류가 발생했습니다",
                details=str(e),
            ).dict(),
        )
