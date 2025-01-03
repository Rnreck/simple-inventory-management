import os
from datetime import timedelta

class Config:
    # 配置数据库连接
    MYSQL_HOST = '127.0.0.1' 
    MYSQL_PORT = 4000 
    MYSQL_USER = 'root' 
    MYSQL_PASSWORD = '' 
    MYSQL_DB = 'inventory'

    # 添加 JWT 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ERROR_MESSAGE_KEY = 'message'
