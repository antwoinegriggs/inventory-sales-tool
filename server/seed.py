#!/usr/bin/env python3
# Standard library imports
from random import randint,choice
# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import *

def create_customer(user):
    return Customer(name=fake.first_name()+' '+fake.last_name(), user=user)

def create_inventory(user):
    return ProductInventory(
        product_name=fake.word(),
        product_number=randint(1000, 9999),
        product_quantity=randint(1, 100),
        product_price=randint(1, 100),
        user=user
    )

def create_order(user, customers, inventory):
    order = SalesOrder(
        date=fake.date_between(start_date='-30d', end_date='today'),
        order_number=fake.uuid4(),
        user=user,
        customer=choice(customers)
    )

    # Add random products from inventory to the order
    # num_products = randint(1, 5)
    order.order_items = []

    # for _ in range(num_products):
    product = choice(inventory)
    quantity = randint(1, 10)
    amount = quantity * product.product_price

        # Create an order item
    order_item = {
            'product_inventory': product,
            'quantity': quantity,
            'amount': amount
        }

    order.quantity = quantity  
    order.amount = amount 
    order.product_inventory_id = product.id
    order.order_items.append(order_item)

    db.session.add(order)
    db.session.commit()
        
        # Populate the join table
    customer_inventory_order_entry = {
            'customer_id': order.customer.id,
            'product_inventory_id': product.id,
            'sales_order_id': order.id
        }
    db.session.execute(customer_inventory_order.insert().values(customer_inventory_order_entry))

    db.session.add(order)
    db.session.commit()

    return order


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        db.drop_all()
        db.create_all()


        print("Starting seed...")
        # Create users with unique usernames
        users = []

        # Append a unique number to the username
        for i in range(3):
            username = fake.first_name() + str(i)
            # Check if the username already exists
            while User.query.filter_by(username=username).first():  
                # Generate a new username if it exists
                username = fake.first_name() + str(i)  
            user = User(
                username=username
    )

            user.password_hash = username + 'password'

            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        # Create customers and associate them with users
        customers = [create_customer(user) for user in users]
        db.session.add_all(customers)
        db.session.commit()

        # Create inventory
        for user in users:
            products = [create_inventory(user) for _ in range(2)]
            for product in products:
                product.user_id = user.id
            db.session.add_all(products)
            db.session.commit()
            user.inventory.extend(products)
            db.session.commit()

        # Create 2 random orders for each user 
        for user in users:
            inventory = ProductInventory.query.filter_by(user=user).all()
            for _ in range(2):
                order = create_order(user, customers, inventory)
                db.session.add(order)
                db.session.commit()

    print("Seed completed successfully.")
