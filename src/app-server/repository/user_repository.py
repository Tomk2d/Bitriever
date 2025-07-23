import logging
from typing import List, Dict, Any
from database.database_connection import db
from model.Users import Users


class UserRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_user(self, user_data: Users) -> Users:
        try:
            session = db.get_session()

            # 이메일 중복 검사
            existing_user = (
                session.query(Users).filter(Users.email == user_data.email).first()
            )
            if existing_user:
                session.close()
                raise ValueError("이미 존재하는 이메일입니다.")

            # 닉네임 중복 검사
            existing_nickname = (
                session.query(Users)
                .filter(Users.nickname == user_data.nickname)
                .first()
            )
            if existing_nickname:
                session.close()
                raise ValueError("이미 존재하는 닉네임입니다.")

            # 사용자 저장
            session.add(user_data)
            session.commit()
            session.refresh(user_data)  # ID 등 생성된 값들을 가져옴

            self.logger.info(f"사용자 저장 완료: {user_data.email}")

            return user_data

        except ValueError as e:
            raise e
        except Exception as e:
            self.logger.error(f"사용자 저장 중 에러 발생: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    def find_by_email(self, email: str) -> Users:
        try:
            session = db.get_session()
            user = session.query(Users).filter(Users.email == email).first()
            return user
        except Exception as e:
            self.logger.error(f"이메일로 사용자 조회 중 에러 발생: {e}")
            raise e
        finally:
            session.close()

    def find_by_id(self, user_id: str) -> Users:
        try:
            session = db.get_session()
            user = session.query(Users).filter(Users.id == user_id).first()
            return user
        except Exception as e:
            self.logger.error(f"ID로 사용자 조회 중 에러 발생: {e}")
            raise e
        finally:
            session.close()

    def find_by_nickname(self, nickname: str) -> Users:
        try:
            session = db.get_session()
            user = session.query(Users).filter(Users.nickname == nickname).first()
            return user
        except Exception as e:
            self.logger.error(f"닉네임으로 사용자 조회 중 에러 발생: {e}")
            raise e
        finally:
            session.close()
