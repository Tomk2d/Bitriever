import logging
from typing import List, Dict, Any
from model.Coins import Coins


class CoinService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._coin_repository = None  # lazy loading

    @property
    def coin_repository(self):
        if self._coin_repository is None:
            from dependencies import get_coin_repository

            self._coin_repository = get_coin_repository()
        return self._coin_repository

    def save_all_coin_list(self, fetched_data_list: List[Dict[Any, Any]]):
        try:
            coin_list = [
                Coins(
                    symbol=data.get("baseCurrencyCode"),
                    quote_currency=data.get("quoteCurrencyCode"),
                    market_code=data.get("pair"),
                    korean_name=data.get("koreanName"),
                    english_name=data.get("englishName"),
                    img_url=f"/data/image/{data.get('baseCurrencyCode')}.png",
                    exchange=data.get("exchange"),
                )
                for data in fetched_data_list
                if data.get("exchange") == "UPBIT"
            ]

            saved_coin_list = self.coin_repository.save_coin_list(coin_list)

            return saved_coin_list
        except Exception as e:
            self.logger.error(f"코인 목록 저장 중 에러 발생: {e}")
            raise e
