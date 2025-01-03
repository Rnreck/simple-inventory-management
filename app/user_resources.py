from flask_restful import Resource, reqparse
from app.db import get_db
from app.models import User
from flask import json, make_response, g
from functools import wraps
from flask import current_app, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)

def get_current_user_from_db():
    """
    从数据库获取当前用户信息
    """
    try:
        user_id = get_jwt_identity()
        if user_id is None:
            return None
            
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    except Exception as e:
        print(f"Error in get_current_user_from_db: {e}")
        return None

def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = get_current_user_from_db()
        if not current_user:
            return {'message': '用户不存在或token无效'}, 401
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = get_current_user_from_db()
        if not current_user:
            return {'message': '用户不存在或token无效'}, 401
        if current_user['role'] != 'admin':
            return {'message': '需要管理员权限'}, 403
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated

class UserRegisterAPI(Resource):
    def post(self):
        """
        用户注册
        ---
        tags:
          - Users
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: 用户名
                password:
                  type: string
                  description: 密码
                role:
                  type: string
                  enum: [admin, user]
                  default: user
                  description: 用户角色
        responses:
          201:
            description: 用户注册成功
          400:
            description: 用户名已存在或其他错误
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, help='用户名必需')
        parser.add_argument('password', required=True, type=str, help='密码必需')
        parser.add_argument('role', type=str, choices=['admin', 'user'], default='user')
        
        args = parser.parse_args()
        
        # 先检查用户名是否已存在
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM users WHERE username = %s', (args['username'],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            return {'message': '用户名已存在'}, 400
            
        # 如果用户名不存在，继续注册流程
        user = User(args['username'], args['password'], args['role'])
        
        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)',
                (user.username, user.password_hash, user.role)
            )
            connection.commit()
            cursor.close()
            return {'message': '用户注册成功'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

class UserLoginAPI(Resource):
    def post(self):
        """
        用户登录
        ---
        tags:
          - Users
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: 用户名
                password:
                  type: string
                  description: 密码
        responses:
          200:
            description: 登录成功
            schema:
              type: object
              properties:
                token:
                  type: string
                  description: JWT token
                message:
                  type: string
                  description: 成功消息
          401:
            description: 用户名或密码错误
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str)
        parser.add_argument('password', required=True, type=str)
        
        args = parser.parse_args()
        
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (args['username'],))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data and check_password_hash(user_data['password_hash'], args['password']):
            access_token = create_access_token(identity=str(user_data['id']))
            return {
                'token': access_token,
                'message': '登录成功',
                'user': {
                    'id': user_data['id'],
                    'username': user_data['username'],
                    'role': user_data['role']
                }
            }
        
        return {'message': '用户名或密码错误'}, 401

class UserProfileAPI(Resource):
    @jwt_required()
    def get(self):
        """
        获取当前用户信息
        ---
        tags:
          - Users
        security:
          - Bearer: []
        responses:
          200:
            description: 用户信息
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: 用户ID
                username:
                  type: string
                  description: 用户名
                role:
                  type: string
                  description: 用户角色
          401:
            description: 未授权或用户不存在
        """
        user = get_current_user_from_db()
        if not user:
            return {'message': '用户不存在'}, 401
        return {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        } 