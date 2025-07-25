import os
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import logging
from typing import Annotated, Any
from fastapi import Depends
from dependencies import get_user_service, get_trading_histories_service
from dto.http_response import ErrorResponse, SuccessResponse
from dto.user_dto import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    LoginResponse,
    UpdateTradingHistoryRequest,
)
from dto.exchange_credentials_dto import ExchangeProvider

router = APIRouter(prefix="/user")
load_dotenv()
logger = logging.getLogger(__name__)


@router.post("/signup")
async def signup(
    user_service: Annotated[Any, Depends(get_user_service)],
    user_data: SignupRequest,
):
    try:
        saved_user_info = user_service.signup(user_data)
        return SuccessResponse(
            data=saved_user_info, message="회원가입이 완료되었습니다"
        )
    except ValueError as e:
        # 비즈니스 로직 에러 (400 Bad Request)
        logger.warning(f"회원가입 검증 실패: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "VALIDATION_ERROR",
                "message": str(e),
                "details": "입력 데이터를 확인해주세요",
            },
        )
    except Exception as e:
        # 시스템 에러 (500 Internal Server Error)
        logger.error(f"회원가입 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다",
            },
        )


@router.post("/login")
async def login(
    user_service: Annotated[Any, Depends(get_user_service)],
    login_data: LoginRequest,
):
    """로그인 API"""
    try:
        user_info = user_service.login(login_data.email, login_data.password)
        return SuccessResponse(data=user_info, message="로그인이 완료되었습니다")
    except ValueError as e:
        # 비즈니스 로직 에러 (400 Bad Request)
        logger.warning(f"로그인 검증 실패: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "LOGIN_FAILED",
                "message": str(e),
                "details": "이메일 또는 비밀번호를 확인해주세요",
            },
        )
    except Exception as e:
        # 시스템 에러 (500 Internal Server Error)
        logger.error(f"로그인 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "로그인 중 오류가 발생했습니다",
            },
        )


@router.get("/check-email")
async def check_email_duplicate(
    user_service: Annotated[Any, Depends(get_user_service)],
    email: str,
):
    """이메일 중복 검사"""
    try:
        is_duplicate = user_service.check_email_duplicate(email)
        return SuccessResponse(
            data={"email": email, "is_duplicate": is_duplicate},
            message="이메일 중복 검사가 완료되었습니다",
        )
    except Exception as e:
        logger.error(f"이메일 중복 검사 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "이메일 중복 검사 중 오류가 발생했습니다",
            },
        )


@router.get("/check-nickname")
async def check_nickname_duplicate(
    user_service: Annotated[Any, Depends(get_user_service)],
    nickname: str,
):
    """닉네임 중복 검사"""
    try:
        is_duplicate = user_service.check_nickname_duplicate(nickname)
        return SuccessResponse(
            data={"nickname": nickname, "is_duplicate": is_duplicate},
            message="닉네임 중복 검사가 완료되었습니다",
        )
    except Exception as e:
        logger.error(f"닉네임 중복 검사 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "닉네임 중복 검사 중 오류가 발생했습니다",
            },
        )


"""======================== 거래내역 API ============================"""


@router.get("/getTradingHistory/{user_id}")
async def get_trading_history(
    user_id: str,
    trading_histories_service: Annotated[Any, Depends(get_trading_histories_service)],
):
    """사용자의 모든 거래내역 조회"""
    try:
        all_trading_histories_data = (
            trading_histories_service.get_all_trading_histories_by_user_formatted(
                user_id
            )
        )

        return SuccessResponse(
            data=all_trading_histories_data,
            message=f"거래내역 조회 완료 (총 {all_trading_histories_data['total_count']}개)",
        )
    except Exception as e:
        logger.error(f"거래내역 조회 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래내역 조회 중 오류가 발생했습니다",
                "details": str(e),
            },
        )


@router.post("/updateTradingHistory")
async def update_trading_history(
    request: UpdateTradingHistoryRequest,
    trading_histories_service: Annotated[Any, Depends(get_trading_histories_service)],
    user_service: Annotated[Any, Depends(get_user_service)],
):
    try:
        try:
            exchange_provider = ExchangeProvider[request.exchange_provider_str.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail={
                    "status_code": 400,
                    "error_code": "INVALID_EXCHANGE_PROVIDER",
                    "message": "잘못된 거래소명입니다",
                    "details": "UPBIT, BITHUMB, BINANCE, OKX 중 하나를 입력해주세요",
                },
            )

        # 사용자의 마지막 거래내역 업데이트 시간 조회
        user = user_service.user_repository.find_by_id(request.user_id)
        start_time = user.last_trading_history_update_at if user else None

        trading_histies = trading_histories_service.get_trading_histories(
            request.user_id, request.exchange_provider_str, start_time
        )
        processed_trading_histies = trading_histories_service.process_trading_histories(
            request.user_id, request.exchange_provider_str, trading_histies
        )

        saved_trading_histories = trading_histories_service.save_trading_histories(
            processed_trading_histies
        )

        all_trading_histories_data = (
            trading_histories_service.get_all_trading_histories_by_user_formatted(
                request.user_id
            )
        )

        user_service.update_user_trading_history_updated_at(request.user_id)

        return SuccessResponse(
            data={
                "saved_count": len(saved_trading_histories),
                **all_trading_histories_data,
            },
            message=f"{exchange_provider.name} 거래내역 업데이트 완료 (저장: {len(saved_trading_histories)}개, 전체: {all_trading_histories_data['total_count']}개)",
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"거래내역 업데이트 중 시스템 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "status_code": 500,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": "거래내역 업데이트 중 오류가 발생했습니다",
                "details": str(e),
            },
        )
