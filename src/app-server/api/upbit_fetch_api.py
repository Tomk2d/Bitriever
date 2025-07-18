import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv, get_key
from datetime import datetime
from service.upbit_service import UpbitService
import logging
from typing import Annotated
from fastapi import Depends
from dependencies import get_upbit_service
from dto.http_response import ErrorResponse, SuccessResponse
from utils.exceptions import UpbitAPIException, AuthenticationException

router = APIRouter()
load_dotenv()
logger = logging.getLogger(__name__)


@router.get("/allTradingHistory")
async def fetch_trading_history(
    upbit_service: Annotated[UpbitService, Depends(get_upbit_service)]
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


@router.get("/order")
async def fetch_api():

    server_url = os.getenv("UPBIT_SERVER_URL", "")

    payload = {
        "access_key": os.getenv("UPBIT_ACCESS_KEY"),
        "nonce": str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, os.getenv("UPBIT_SECRET_KEY", ""))
    authorization = "Bearer {}".format(jwt_token)
    headers = {
        "Authorization": authorization,
    }

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    res.json()

    return res.json()


@router.get("/order2")
async def fetch_api2():
    server_url = os.getenv("UPBIT_SERVER_URL", "")
    access_key = os.getenv("UPBIT_ACCESS_KEY", "")
    secret_key = os.getenv("UPBIT_SECRET_KEY", "")

    params = {"market": "KRW-BTC"}
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        "access_key": access_key,
        "nonce": str(uuid.uuid4()),
        "query_hash": query_hash,
        "query_hash_alg": "SHA512",
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = "Bearer {}".format(jwt_token)
    headers = {
        "Authorization": authorization,
    }

    res = requests.get(server_url + "/v1/orders/chance", params=params, headers=headers)
    return res.json()


@router.get("/order3")
async def fetch_api3():
    server_url = os.getenv("UPBIT_SERVER_URL", "")
    access_key = os.getenv("UPBIT_ACCESS_KEY", "")
    secret_key = os.getenv("UPBIT_SECRET_KEY", "")

    params = {"uuid": "d098ceaf-6811-4df8-97f2-b7e01aefc03f"}
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        "access_key": access_key,
        "nonce": str(uuid.uuid4()),
        "query_hash": query_hash,
        "query_hash_alg": "SHA512",
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = "Bearer {}".format(jwt_token)
    headers = {
        "Authorization": authorization,
    }

    res = requests.get(server_url + "/v1/order", params=params, headers=headers)
    return res.json()


@router.get("/order4")
async def fetch_api4():
    server_url = os.getenv("UPBIT_SERVER_URL", "")
    access_key = os.getenv("UPBIT_ACCESS_KEY", "")
    secret_key = os.getenv("UPBIT_SECRET_KEY", "")

    params = {
        "states[]": ["done", "cancel"],
    }

    # params = {"states[]": ["done", "cancel"]}
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        "access_key": access_key,
        "nonce": str(uuid.uuid4()),
        "query_hash": query_hash,
        "query_hash_alg": "SHA512",
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = "Bearer {}".format(jwt_token)
    headers = {
        "Authorization": authorization,
    }

    res = requests.get(server_url + "/v1/orders/closed", params=params, headers=headers)
    for r in res.json():
        print("주문 종류 : ", r.get("side"))
        print("주문 타입 : ", r.get("ord_type"))
        print("코인 코드 : ", r.get("market"))
        print("당시 가격 : ", r.get("price"))
        print("체결된 수 : ", r.get("executed_volume"))
        print("체결 안된 남은 수량 : ", r.get("remaining_volume"))
        print("주문 상태 : ", r.get("state"))
        print("주문 시간 : ", r.get("created_at"))
        print("--------------------------------")
        print(r)
        print("================================================")
    return res.json()
