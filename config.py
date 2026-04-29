import json
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@127.0.0.1:3306/mysql")
    DATABASES = json.loads(os.getenv("DATABASES", "{}"))
    MAX_ROWS = int(os.getenv("MAX_ROWS", "200"))
    SQL_READONLY = os.getenv("SQL_READONLY", "false").lower() == "true"
