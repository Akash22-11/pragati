from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
   
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:5500"]

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # Email
    MAIL_EMAIL: str
    MAIL_PASSWORD: str
    ADMIN_EMAIL: str

    # Pragati AI (open-weight model behind an OpenAI-compatible endpoint)
    AI_BASE_URL: str = "http://localhost:11434/v1"
    AI_MODEL: str = "qwen2.5:7b-instruct"
    AI_API_KEY: str = ""
    AI_TIMEOUT_SECONDS: float = 60.0

    class Config:
        env_file = ".env"


settings = Settings()
