import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")

class Config:
    DEBUG: bool = False
    TESTING: bool = False
    # SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("MY_LOCAL_SQL")

class DevelopmentConfig(Config):
    DEBUG: bool = True

class ProductionConfig(Config):
    pass