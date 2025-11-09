import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    PLAID_CLIENT_ID: str
    PLAID_SECRET: str
    PLAID_ENV: str = "sandbox"
    PLAID_PRODUCTS: str = "transactions"
    PLAID_COUNTRY_CODES: str = "US"
    APP_HOST: str = "http://localhost:5173"
    DB_PATH: str = "plaid_lab.sqlite"

    class Config:
        env_file = ".env"


settings = Settings()
