from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db, bcrypt

# Models go here!


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)

    # Add relationships to associate users with their data (customers, sales orders, and inventory)
    customers = db.relationship('Customer', backref='user')
    sales_orders = db.relationship('SalesOrder', backref='user')
    inventory = db.relationship('ProductInventory', backref='user')


    # Serialization rules to control output
    serialize_rules = ('-customers.user', '-sales_orders.user', '-inventory.user', '-password_hash')

    @hybrid_property
    def password_hash(self):
        raise AttributeError
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))


class ProductInventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(20))
    product_number = db.Column(db.Integer)
    product_quantity = db.Column(db.Integer)
    product_price = db.Column(db.Integer)

    ###
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Many-to-Many Customer
    inventory_customer = db.relationship(
        'Customer', secondary='customer_inventory_orders', overlaps='customer_inventory')

    # One-to-Many SalesOrder
    inventory_orders = db.relationship('SalesOrder', backref='orders')

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    ###
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Many-to-Many ProductInventory
    customer_inventory = db.relationship(
        'ProductInventory', secondary='customer_inventory_orders', overlaps='customer_inventory')
    # One-to-Many SaleOrders
    customer_orders = db.relationship('SalesOrder', backref='customer')

class SalesOrder(db.Model):
    __tablename__ = 'sales_orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    order_number = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @property
    def customer_name(self):
        return self.customer.name
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    @property
    def product_name(self):
        return self.product.product_name
    product_inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))

    quantity = db.Column(db.Integer)
    amount = db.Column(db.Float)

    # Many-to-Many Custoemr
    customer_order = db.relationship(
        'Customer', secondary='customer_inventory_orders', overlaps='customer_inventory, inventory_customer')
    
# Join Table Customer, Inventory, Order
customer_inventory_order = db.Table(
    'customer_inventory_orders',
    db.Column("id", db.Integer, primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customers.id')),
    db.Column('product_inventory_id', db.Integer,
              db.ForeignKey('inventory.id')),
    db.Column('sales_order_id', db.Integer, db.ForeignKey('sales_orders.id'))
)