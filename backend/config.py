"""
配置文件
"""
import os
from pathlib import Path
from typing import List, Optional
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用程序设置"""
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./water_quality.db"
    DATABASE_ECHO: bool = False
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Water Quality Management System"
    PROJECT_VERSION: str = "1.0.0"
    DESCRIPTION: str = "Enterprise-grade water quality data management system"
    DEBUG: bool = True
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin Configuration
    ADMIN_EMAIL: str = "admin@waterquality.com"
    ADMIN_PASSWORD: str = "admin123"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "{time} | {level} | {message}"
    LOG_RETENTION: int = 30
    
    # Pagination Configuration
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File paths
    BASE_DIR: Path = Path(__file__).resolve().parent
    LOG_DIR: Path = BASE_DIR / "logs"
    DATA_DIR: Path = BASE_DIR / "data"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()

# 确保目录存在
settings.LOG_DIR.mkdir(exist_ok=True)
settings.DATA_DIR.mkdir(exist_ok=True) 