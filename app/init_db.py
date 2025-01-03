import pymysql
from app.config import Config

def init_db():
    # 连接到服务器（不指定数据库）
    connection = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD
    )
    
    try:
        with connection.cursor() as cursor:
            # 读取schema.sql文件
            with open('app/schema.sql', 'r', encoding='utf-8') as f:
                # 分割SQL语句
                sql_commands = f.read().split(';')
                
                # 执行每个SQL命令
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
                
        connection.commit()
        print("数据库初始化成功！")
        
    except Exception as e:
        print(f"初始化数据库时出错: {e}")
    
    finally:
        connection.close()

if __name__ == '__main__':
    init_db() 