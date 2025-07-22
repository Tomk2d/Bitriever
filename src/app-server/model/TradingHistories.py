from sqlalchemy import (
    Column,
    String,
    Integer,
    SmallInteger,
    Numeric,
    TIMESTAMP,
    func,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database_connection import db


class TradingHistories(db.Base):
    __tablename__ = "trading_histories"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 내부용 기본키

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    coin_id = Column(
        Integer, ForeignKey("coins.id", ondelete="CASCADE"), nullable=False
    )

    exchange = Column(String(20), nullable=False, default="upbit")  # 거래소 이름
    trade_uuid = Column(String(100), nullable=False)  # 외부 체결 고유 ID

    trade_type = Column(SmallInteger, nullable=False)  # 0: 매수, 1: 매도

    price = Column(Numeric(20, 8), nullable=False)
    quantity = Column(Numeric(20, 8), nullable=False)
    total_price = Column(Numeric(20, 8), nullable=False)  # price * quantity

    fee = Column(Numeric(20, 8), default=0)  # 수수료
    trade_time = Column(TIMESTAMP, nullable=False)  # 체결시간
    created_at = Column(TIMESTAMP, default=func.now())  # 해당 칼럼 생성시간

    # 관계 설정
    user = relationship("Users", back_populates="trading_histories")
    coin = relationship("Coins", back_populates="trading_histories")

    # 유니크 제약조건
    __table_args__ = (
        UniqueConstraint(
            "user_id", "exchange", "trade_uuid", name="uq_user_exchange_trade_uuid"
        ),
    )

    def __repr__(self):
        return f"<TradingHistory(id={self.id}, user_id={self.user_id}, trade_uuid={self.trade_uuid})>"
