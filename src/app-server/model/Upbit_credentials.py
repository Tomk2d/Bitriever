from sqlalchemy import Column, String, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database_connection import db


class UpbitCredentials(db.Base):
    __tablename__ = "upbit_credentials"

    # users의 uuid와 동일한 값을 가짐. users 삭제시, 삭제. 이것도 pk 임
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    encrypted_access_key = Column(Text, nullable=False)  # 암호화 하여 저장
    encrypted_secret_key = Column(Text, nullable=False)  # 암호화 하여 저장

    created_at = Column(TIMESTAMP, default=func.now())
    last_updated_at = Column(TIMESTAMP)

    # 관계 설정
    user = relationship("Users", back_populates="upbit_credentials")

    def __repr__(self):
        return f"<UpbitCredentials(user_id={self.user_id})>"
