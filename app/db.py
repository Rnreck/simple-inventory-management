from flask import current_app, g
import pymysql
from pymysql.cursors import DictCursor

def get_db():
    if 'db' not in g:
        config = current_app.config
        g.db = pymysql.connect(
            host=config['MYSQL_HOST'],
            port=config['MYSQL_PORT'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DB'],
            cursorclass=DictCursor
        )
    return g.db 