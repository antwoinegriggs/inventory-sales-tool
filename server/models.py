from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!
class ProductInventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20))
    product_number = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)
    product_price = db.Column(db.Integer)

    # Many-to-Many Customer
    inventory_customer = db.relationship(
        'Customer', secondary='customer_inventory_orders', overlaps='customer_inventory')

    # One-to-Many SalesOrder
    inventory_orders = db.relationship('SalesOrder')

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # Many-to-Many ProductInventory
    customer_inventory = db.relationship(
        'ProductInventory', secondary='customer_inventory_orders', overlaps='customer_inventory')
    # One-to-Many SaleOrders
    customer_orders = db.relationship('SalesOrder')
