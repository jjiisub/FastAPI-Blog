from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    '''
    .env 파일 로드

        Attributes:
            ACCESS_TOKEN_EXPIRE_SECONDS (int): 로그인 세션 유지 기간 (redis 만료)
            SQLALCHEMY_DATABASE_URL (str): PostgreSQL DB 연결 주소
            PAGE_SIZE (str): pagination 단위
    '''
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 0
    SQLALCHEMY_DATABASE_URL: str = ""
    PAGE_SIZE: int = 1

    model_config = SettingsConfigDict(env_file=".env")