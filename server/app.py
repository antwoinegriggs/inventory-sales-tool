#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from flask import request, session, jsonify, make_response
from config import app, db, api
# Add your model imports
from models import *

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        new_user = User(
            username = data.get('username')
        )
        
        new_user.password_hash = data.get('password')
        
        db.session.add(new_user)
        
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return make_response({"message": "422 (Unprocessable Entity)"}, 422)
        
        session['user_id'] = new_user.id
        user_dict = new_user.to_dict()

        return make_response(jsonify(user_dict), 201)


class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)

class Login(Resource):
    def post(self):
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter(User.username == username).first()
        
        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)

class Logout(Resource):
    def delete(self):
        if session['user_id'] == None:
            return make_response({"message": "401 (Unauthorized)"}, 401)
        else:
            session['user_id'] = None
            return make_response({"message": "204 (No Content)"}, 204)

class ProductInventoryList(Resource):
    def get(self, product_inventory_id=None):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            if product_inventory_id is None:
              
                products = ProductInventory.query.filter_by(user_id=user.id).all()
                product_list = [product.to_dict() for product in products]
                return product_list, 200
            else:
                
                product = ProductInventory.query.filter_by(id=product_inventory_id, user_id=user.id).first()
                if product:
                    return product.to_dict(), 200
                else:
                    return {"message": "ProductInventory not found"}, 404
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)
        
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.id == session.get('user_id')).first()

        if user:
            product = ProductInventory(
                product_name=data['product_name'],
                product_number=data['product_number'],
                product_quantity=data['product_quantity'],
                product_price=data['product_price'],
                user=user
            )

            db.session.add(product)

            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                return make_response({"message": "422 (Unprocessable Entity)"}, 422)

            return make_response(jsonify(product.to_dict()), 201)
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)
        
        
class Product(Resource):
    def put(self, product_inventory_id):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            data = request.get_json()
            product = ProductInventory.query.filter_by(id=product_inventory_id, user_id=user.id).first()
            if product:
                # Update the product details based on the data from the request
                product.product_name = data['product_name']
                product.product_number = data['product_number']
                product.product_quantity = data['product_quantity']
                product.product_price = data['product_price']

                db.session.commit()

                return product.to_dict(), 200
            else:
                return {"message": f"ProductInventory not found for ID: {product_inventory_id}"}, 404
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)

    def delete(self, product_inventory_id):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            product = ProductInventory.query.filter_by(id=product_inventory_id, user_id=user.id).first()
    
            if product:
                db.session.delete(product)
                db.session.commit()
                return {"message": "ProductInventory deleted"}, 204
            else:
                return {"message": f"ProductInventory not found for ID: {product_inventory_id}"}, 404
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)

class CustomerList(Resource):
    def get(self, customer_id=None):
        user = User.query.filter(User.id == session.get('user_id')).first()

        if user:
            if customer_id is None:
              
                customers = Customer.query.filter_by(user_id=user.id).all()
                customer_list = [customer.to_dict() for customer in customers]
                return customer_list, 200
            else:
             
                customer = Customer.query.filter_by(id=customer_id, user_id=user.id).first()
                if customer:
                    return customer.to_dict(), 200
                else:
                    return {"message": "Customer not found"}, 404
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)
        
    def post(self):
        data = request.get_json()
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            
            new_customer = Customer(
                name=data['name'],
                user=user
            )

            db.session.add(new_customer)

            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                return make_response({"message": "422 (Unprocessable Entity)"}, 422)

            return make_response(jsonify(new_customer.to_dict()), 201)
        else:
            return make_response({"message": "401 (Unauthorized)"}, 401)

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(ProductInventoryList, '/product_inventory', endpoint='product_inventory')
api.add_resource(Product, '/product_inventory/<int:product_inventory_id>', endpoint='product')
api.add_resource(CustomerList, '/customers', endpoint='customers')
# api.add_resource(CustomerList, '/customers/<int:customer_id>', endpoint='customer')




if __name__ == '__main__':
    app.run(port=5555, debug=True)

