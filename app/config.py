from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AI_API_KEY: str | None = None
    AI_API_BASE_URL: str = "https://api.openai.com/v1"
    AI_MODEL: str = "gpt-5-mini"
    BORROW_LIMIT: int = 3
    BORROW_DAYS: int = 14
    RESERVATION_HOLD_HOURS: int = 24
    FINE_PER_DAY: float = 5.0
    CORS_ORIGINS: str = "*"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
