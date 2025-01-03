from flask_restful import Resource, reqparse
from app.db import get_db
from flask import json, make_response
from app.user_resources import admin_required, token_required

class CategoriesAPI(Resource):
    @token_required
    def get(self):
        """
        获取所有产品分类
        ---
        tags:
          - Categories
        security:
          - Bearer: []
        responses:
          200:
            description: 分类列表
            schema:
              type: object
              properties:
                categories:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
          401:
            description: 未授权
        """
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY id ASC")
        categories = cursor.fetchall()
        cursor.close()

        response = make_response(
            json.dumps(
                {"categories": categories},
                ensure_ascii=False
            )
        )
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    @admin_required
    def post(self):
        """
        创建新分类
        ---
        tags:
          - Categories
        security:
          - Bearer: []
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: 分类名称
        responses:
          201:
            description: 分类创建成功
          400:
            description: 分类名称已存在
          401:
            description: 未授权
          403:
            description: 需要管理员权限
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str, help="分类名称必需")

        args = parser.parse_args()
        connection = get_db()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO categories (name) VALUES (%s)",
                (args['name'],)
            )
            connection.commit()
            cursor.close()
            return {"message": "分类创建成功"}, 201
        except Exception as e:
            return {"message": str(e)}, 400