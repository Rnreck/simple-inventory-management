from flask_restful import Resource, reqparse
from app.db import get_db
from flask import json, make_response, g
from app.user_resources import token_required
from datetime import datetime

class OrdersAPI(Resource):
    @token_required
    def get(self):
        """
        获取当前用户的订单列表
        ---
        tags:
          - Orders
        security:
          - Bearer: []
        responses:
          200:
            description: 订单列表
            schema:
              type: object
              properties:
                orders:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      user_id:
                        type: integer
                      total_amount:
                        type: number
                      status:
                        type: string
                        enum: [pending, completed, cancelled]
                      created_at:
                        type: string
                        format: date-time
                      items:
                        type: array
                        items:
                          type: object
                          properties:
                            product_id:
                              type: integer
                            product_name:
                              type: string
                            quantity:
                              type: integer
                            price:
                              type: number
          401:
            description: 未授权
        """
        connection = get_db()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT o.*, COUNT(oi.id) as items_count 
            FROM orders o 
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE o.user_id = %s 
            GROUP BY o.id
            ORDER BY o.created_at DESC
        """, (g.current_user['id'],))
        
        orders = cursor.fetchall()
        
        for order in orders:
            cursor.execute("""
                SELECT oi.*, p.name as product_name
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
            """, (order['id'],))
            order['items'] = cursor.fetchall()

        cursor.close()
        
        response = make_response(
            json.dumps(
                {"orders": orders},
                ensure_ascii=False,
                default=str
            )
        )
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    @token_required
    def post(self):
        """
        创建新订单
        ---
        tags:
          - Orders
        security:
          - Bearer: []
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      product_id:
                        type: integer
                        description: 产品ID
                      quantity:
                        type: integer
                        description: 购买数量
              example:
                items:
                  - product_id: 1
                    quantity: 2
                  - product_id: 2
                    quantity: 1
        responses:
          201:
            description: 订单创建成功
            schema:
              type: object
              properties:
                message:
                  type: string
                order_id:
                  type: integer
          400:
            description: 库存不足或其他错误
          401:
            description: 未授权
        """
        parser = reqparse.RequestParser()
        parser.add_argument('items', type=list, required=True, location='json')
        
        args = parser.parse_args()
        connection = get_db()
        cursor = connection.cursor()
        
        try:
            # 开始事务
            connection.begin()
            
            total_amount = 0
            order_items = []
            
            # 检查库存并计算总金额
            for item in args['items']:
                cursor.execute(
                    "SELECT id, price, inventory FROM products WHERE id = %s FOR UPDATE",
                    (item['product_id'],)
                )
                product = cursor.fetchone()
                
                if not product:
                    raise Exception(f"产品ID {item['product_id']} 不存在")
                
                if product['inventory'] < item['quantity']:
                    raise Exception(f"产品ID {item['product_id']} 库存不足")
                
                item_total = float(product['price']) * item['quantity']
                total_amount += item_total
                
                order_items.append({
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'price': float(product['price'])
                })
            
            # 创建订单
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, 'pending')",
                (g.current_user['id'], total_amount)
            )
            order_id = cursor.lastrowid
            
            # 添加订单项并更新库存
            for item in order_items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, item['product_id'], item['quantity'], item['price'])
                )
                
                cursor.execute(
                    "UPDATE products SET inventory = inventory - %s WHERE id = %s",
                    (item['quantity'], item['product_id'])
                )
            
            connection.commit()
            return {"message": "订单创建成功", "order_id": order_id}, 201
            
        except Exception as e:
            connection.rollback()
            return {"message": str(e)}, 400
        finally:
            cursor.close()