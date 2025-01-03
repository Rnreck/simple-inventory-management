from flask import Flask, jsonify, g
from flask_restful import Api
from flasgger import Swagger
from app.resources import ProductsAPI, ProductAPI, ProductsQueryAPI
from app.user_resources import UserRegisterAPI, UserLoginAPI, UserProfileAPI
from flask_jwt_extended import JWTManager
from app.category_resources import CategoriesAPI
from app.order_resources import OrdersAPI
from app.db import get_db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # 设置JSON编码
    app.config['JSON_AS_ASCII'] = False
    app.json.ensure_ascii = False

    # 初始化 JWT
    jwt = JWTManager(app)
    
    # JWT错误处理
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {"message": "无效的token"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return {"message": "token已过期"}, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {"message": "缺少Authorization头部"}, 401

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        try:
            identity = jwt_data["sub"]
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id = %s', (identity,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            print(f"Error in user_lookup_callback: {e}")
            return None

    # 添加JWT回调
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, dict):
            return user.get('id')
        return user

    # 添加数据库连接关闭函数
    @app.teardown_appcontext
    def close_db(error):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    # 初始化 Swagger，添加安全配置
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        # 添加 Swagger UI 配置
        "swagger_ui_config": {
            "persistAuthorization": True,  # 保持认证状态
            "displayRequestDuration": True,
            "filter": True
        }
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "库存管理 API",
            "description": """
            库存管理系统的 API 文档
            
            认证说明:
            1. 先调用 /api/users/login 接口登录获取 token
            2. 点击右上角 "Authorize" 按钮
            3. 在弹出框中输入 Bearer <your_token>
            4. 点击 "Authorize" 确认
            """,
            "version": "1.0.0",
        },
        "tags": [
            {
                "name": "Users",
                "description": "用户管理相关接口"
            },
            {
                "name": "Products",
                "description": "产品管理相关接口"
            },
            {
                "name": "Categories",
                "description": "产品分类相关接口"
            },
            {
                "name": "Orders",
                "description": "订单管理相关接口"
            }
        ],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    @app.route('/')
    def home():
        return jsonify({"message": "欢迎使用库存管理系统"})

    # 初始化 RESTful API
    api = Api(app)
    
    # 用户相关路由
    api.add_resource(UserLoginAPI, '/api/users/login')
    api.add_resource(UserRegisterAPI, '/api/users/register')
    api.add_resource(UserProfileAPI, '/api/users/me')
    
    # 产品相关路由
    api.add_resource(ProductsAPI, '/api/products')
    api.add_resource(ProductAPI, '/api/products/<int:product_id>')
    api.add_resource(ProductsQueryAPI, '/api/products/query')
    
    # 分类和订单路由 - 简化后的路由
    api.add_resource(CategoriesAPI, '/api/categories')  # 只保留基础的分类管理
    api.add_resource(OrdersAPI, '/api/orders')  # 只保留基础的订单管理
    
    @app.after_request
    def after_request(response):
        # 允许本地开发时的跨域请求
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        # 添加缓存控制
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return response
    
    return app