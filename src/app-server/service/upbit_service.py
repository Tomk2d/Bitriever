from typing import List, Dict, Any, Optional
import requests
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
import jwt
import hashlib
import uuid
from urllib.parse import urlencode, unquote
from utils.upbit_http_client import UpbitHttpClient
import logging

load_dotenv()


class UpbitService:
    def __init__(self):
        self.upbit_http_client = UpbitHttpClient()
        self.logger = logging.getLogger(__name__)

    def fetch_user_trading_history(self, access_key: str, secret_key: str):
        params = {
            "states[]": ["done", "cancel"],
        }
        try:
            res = self.upbit_http_client.get(
                "/v1/orders/closed", access_key, secret_key, params, True
            )
            # 여기를 이제 dto 로 매핑하고 반환하는걸로 변경
            for r in res:
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
            return res
        except Exception as e:
            raise e
