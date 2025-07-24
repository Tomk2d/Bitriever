from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Any, List
from dto.exchange_credentials_dto import (
    ExchangeCredentialsRequest,
    ExchangeCredentialsResponse,
    ExchangeProvider,
)
from service.exchange_credentials_service import ExchangeCredentialsService
import logging
from dto.http_response import SuccessResponse, ErrorResponse

router = APIRouter(prefix="/exchange-credentials", tags=["거래소 자격증명"])
logger = logging.getLogger(__name__)


def get_exchange_credentials_service() -> ExchangeCredentialsService:
    """거래소 자격증명 서비스 의존성"""
    return ExchangeCredentialsService()


@router.post("/{user_id}")
async def save_credentials(
    user_id: str,
    request: ExchangeCredentialsRequest,
    service: Annotated[
        ExchangeCredentialsService, Depends(get_exchange_credentials_service)
    ],
):
    """거래소 자격증명 저장/업데이트"""
    try:
        response = service.save_credentials(user_id, request)
        return SuccessResponse(
            data=response,
            message=f"{response.provider_name} 자격증명이 저장되었습니다.",
        )
    except ValueError as e:
        logger.warning(f"거래소 자격증명 저장 검증 에러: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "status_code": 400,
                "error_code": "INVALID_CREDENTIALS",
                "message": str(e),
                "details": "입력된 정보를 확인해주세요",
            },
        )
    except Exception as e:
        logger.error(f"거래소 자격증명 저장 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래소 자격증명 저장 중 오류가 발생했습니다",
                "details": str(e),
            },
        )


@router.get("/{user_id}/{exchange_provider}")
async def get_credentials(
    user_id: str,
    exchange_provider: ExchangeProvider,
    service: Annotated[
        ExchangeCredentialsService, Depends(get_exchange_credentials_service)
    ],
):
    """특정 거래소 자격증명 조회"""
    try:
        credentials = service.get_credentials(user_id, exchange_provider)
        if not credentials:
            raise HTTPException(
                status_code=404,
                detail={
                    "status_code": 404,
                    "error_code": "CREDENTIALS_NOT_FOUND",
                    "message": "해당 거래소의 자격증명을 찾을 수 없습니다",
                    "details": f"사용자 {user_id}의 {exchange_provider.name} 자격증명이 없습니다",
                },
            )

        return SuccessResponse(
            data=credentials, message=f"{credentials.provider_name} 자격증명 조회 완료"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"거래소 자격증명 조회 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래소 자격증명 조회 중 오류가 발생했습니다",
                "details": str(e),
            },
        )


@router.get("/{user_id}")
async def get_all_credentials(
    user_id: str,
    service: Annotated[
        ExchangeCredentialsService, Depends(get_exchange_credentials_service)
    ],
):
    """사용자의 모든 거래소 자격증명 조회"""
    try:
        credentials_list = service.get_all_credentials(user_id)
        return SuccessResponse(
            data=credentials_list,
            message=f"총 {len(credentials_list)}개의 거래소 자격증명 조회 완료",
        )
    except Exception as e:
        logger.error(f"사용자 거래소 자격증명 조회 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래소 자격증명 조회 중 오류가 발생했습니다",
                "details": str(e),
            },
        )


@router.delete("/{user_id}/{exchange_provider}")
async def delete_credentials(
    user_id: str,
    exchange_provider: ExchangeProvider,
    service: Annotated[
        ExchangeCredentialsService, Depends(get_exchange_credentials_service)
    ],
):
    """거래소 자격증명 삭제"""
    try:
        success = service.delete_credentials(user_id, exchange_provider)
        if not success:
            raise HTTPException(
                status_code=404,
                detail={
                    "status_code": 404,
                    "error_code": "CREDENTIALS_NOT_FOUND",
                    "message": "삭제할 거래소 자격증명을 찾을 수 없습니다",
                    "details": f"사용자 {user_id}의 {exchange_provider.name} 자격증명이 없습니다",
                },
            )

        return SuccessResponse(
            data={"deleted": True},
            message=f"{exchange_provider.name} 자격증명이 삭제되었습니다",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"거래소 자격증명 삭제 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래소 자격증명 삭제 중 오류가 발생했습니다",
                "details": str(e),
            },
        )


@router.post("/{user_id}/{exchange_provider}/verify")
async def verify_credentials(
    user_id: str,
    exchange_provider: ExchangeProvider,
    service: Annotated[
        ExchangeCredentialsService, Depends(get_exchange_credentials_service)
    ],
):
    """거래소 자격증명 유효성 검증"""
    try:
        is_valid = service.verify_credentials(user_id, exchange_provider)
        return SuccessResponse(
            data={"is_valid": is_valid},
            message=f"{exchange_provider.name} 자격증명 검증 완료",
        )
    except Exception as e:
        logger.error(f"거래소 자격증명 검증 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래소 자격증명 검증 중 오류가 발생했습니다",
                "details": str(e),
            },
        )
