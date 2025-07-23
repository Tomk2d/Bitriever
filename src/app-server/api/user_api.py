import os
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import logging
from typing import Annotated, Any
from fastapi import Depends
from dependencies import get_user_service
from dto.http_response import ErrorResponse, SuccessResponse
from dto.user_dto import SignupRequest, SignupResponse, LoginRequest, LoginResponse

router = APIRouter()
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
