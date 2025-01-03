from flask_restful import Resource, reqparse
from app.db import get_db
from flask import json, make_response
from app.user_resources import token_required, admin_required


class ProductsAPI(Resource):
    '''
    GET /api/products - 获取所有产品
    '''

    @token_required
    def get(self):
        '''
        获取所有产品
        ---
        tags:
          - Products
        description: 检索所有产品
        responses:
          200:
            description: 产品列表
        '''
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id ASC;")
        rows = cursor.fetchall()
        cursor.close()

        products = [
            {
                "id": row['id'],
                "name": row['name'],
                "inventory": row['inventory'],
                "price": float(row['price'])
            }
            for row in rows
        ]

        response = make_response(
            json.dumps(
                {"products": products},
                ensure_ascii=False
            )
        )
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    '''
    POST /api/products - 添加新产品
    '''

    @admin_required
    def post(self):
        '''
        添加单个产品
        ---
        tags:
          - Products
        description: 添加一个新产品到库存
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                inventory:
                  type: integer
                price:
                  type: number
        responses:
          201:
            description: 产品成功添加
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=str, help="产品名称必需")
        parser.add_argument('inventory', required=True, type=int, help="库存数量必需")
        parser.add_argument('price', required=True, type=float, help="价格必需")

        try:
            args = parser.parse_args()
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO products (name, inventory, price) VALUES (%s, %s, %s);",
                (args['name'], args['inventory'], args['price'])
            )
            connection.commit()
            cursor.close()
            return {"message": "产品成功添加"}, 201
        except Exception as e:
            return {"message": str(e)}, 400


class ProductAPI(Resource):
    '''
    GET /api/products/{id} - 获取单个产品
    '''

    @token_required
    def get(self, product_id):
        '''
        获取单个产品
        ---
        tags:
          - Products
        parameters:
          - name: product_id
            in: path
            type: integer
            required: true
            description: 产品ID
        responses:
          200:
            description: 产品详情
          404:
            description: 产品未找到
        '''
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            product = {
                "id": row['id'],
                "name": row['name'],
                "inventory": row['inventory'],
                "price": float(row['price'])
            }
            response = make_response(
                json.dumps(
                    {"product": product},
                    ensure_ascii=False
                )
            )
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response
        return {"message": "产品未找到"}, 404

    '''
    PUT /api/products/{id} - 更新产品
    '''

    @admin_required
    def put(self, product_id):
        '''
        修改单个产品
        ---
        tags:
          - Products
        parameters:
          - name: product_id
            in: path
            type: integer
            required: true
            description: 要更新的产品ID
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                inventory:
                  type: integer
                price:
                  type: number
        responses:
          200:
            description: 产品成功更新
          404:
            description: 产品未找到
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('inventory', type=int)
        parser.add_argument('price', type=float)

        try:
            args = parser.parse_args()
            connection = get_db()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            if not cursor.fetchone():
                cursor.close()
                return {"message": "产品未找到"}, 404

            updates = []
            values = []
            for key, value in args.items():
                if value is not None:
                    updates.append(f"{key} = %s")
                    values.append(value)

            if updates:
                values.append(product_id)
                update_query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
                cursor.execute(update_query, tuple(values))
                connection.commit()

            cursor.close()
            return {"message": "产品成功更新"}, 200
        except Exception as e:
            return {"message": str(e)}, 400

    '''
    DELETE /api/products/{id} - 删除产品
    '''

    @admin_required
    def delete(self, product_id):
        '''
        删除单个产品
        ---
        tags:
          - Products
        parameters:
          - name: product_id
            in: path
            type: integer
            required: true
            description: 要删除的产品ID
        responses:
          200:
            description: 产品成功删除
          404:
            description: 产品未找到
        '''
        try:
            connection = get_db()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            if not cursor.fetchone():
                cursor.close()
                return {"message": "产品未找到"}, 404

            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            connection.commit()
            cursor.close()
            return {"message": "产品成功删除"}, 200
        except Exception as e:
            return {"message": str(e)}, 400


class ProductsQueryAPI(Resource):
    '''
    GET /api/products/query - 条件查询产品
    '''

    def get(self):
        '''
        条件查询产品
        ---
        tags:
          - Products
        description: 基于name、inventory和price查询产品
        parameters:
          - name: name
            in: query
            type: string
            required: false
            description: 产品名称（模糊匹配）
          - name: inventory
            in: query
            type: integer
            required: false
            description: 最小库存数量
          - name: price_min
            in: query
            type: number
            required: false
            description: 最低价格
          - name: price_max
            in: query
            type: number
            required: false
            description: 最高价格
        responses:
          200:
            description: 匹配查询条件的产品列表
          404:
            description: 未找到匹配的产品
        '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, location='args')
            parser.add_argument('inventory', type=int, location='args')
            parser.add_argument('price_min', type=float, location='args')
            parser.add_argument('price_max', type=float, location='args')

            args = parser.parse_args()

            query = "SELECT * FROM products WHERE 1=1"
            values = []

            if args['name']:
                query += " AND name LIKE %s"
                values.append(f"%{args['name']}%")

            if args['inventory'] is not None:
                query += " AND inventory >= %s"
                values.append(args['inventory'])

            if args['price_min'] is not None:
                query += " AND price >= %s"
                values.append(args['price_min'])

            if args['price_max'] is not None:
                query += " AND price <= %s"
                values.append(args['price_max'])

            query += " ORDER BY id ASC"

            connection = get_db()
            cursor = connection.cursor()
            cursor.execute(query, tuple(values))
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                return {"message": "未找到匹配的产品"}, 404

            products = [
                {
                    "id": row['id'],
                    "name": row['name'],
                    "inventory": row['inventory'],
                    "price": float(row['price'])
                }
                for row in rows
            ]

            response = make_response(
                json.dumps(
                    {"products": products},
                    ensure_ascii=False
                )
            )
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            return response

        except Exception as e:
            return {"message": f"查询出错: {str(e)}"}, 400