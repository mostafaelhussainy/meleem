from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    DB_HOST: str       
    DB_PORT: int         
    DB_NAME: str           
    DB_USER: str        
    DB_PASSWORD: str 
    DB_MIN_CONNECTIONS: int
    DB_MAX_CONNECTIONS: int

    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int 

    # Extra settings
    CORS_ORIGINS: List[str] = Field(default=["*"])
    PASSWORD_HASH_ROUNDS: int = Field(default=12)

    class Config:
        env_file = ".env"

settings = Settings() 