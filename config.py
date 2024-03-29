from pydantic import BaseSettings


class DBSettings(BaseSettings):
    database_user: str
    database_password: str
    database_host: str
    database_port: str
    database_db: str

    class Config:
        env_file = ".env"


class BucketSettings(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket_name: str

    class Config:
        env_file = ".env"


class TokenSettings(BaseSettings):
    secret_key: str
    secret_key_2: str
    algorithm: str
    access_token_expire_minutes: int
    guest_access_token_expire_minutes: int

    class Config:
        env_file = ".env"


class SmsSettings(BaseSettings):
    SMS_EMAIL: str
    SMS_PWD: str

    class Config:
        env_file = ".env"


class BannerSettings(BaseSettings):
    BASE_URL: str

    class Config:
        env_file = ".env"
