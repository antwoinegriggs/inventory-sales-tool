#!/usr/bin/env python3
# Standard library imports
from random import randint
# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import *

def create_customer(user):
    return Customer(name=fake.first_name()+' '+fake.last_name(), user=user)

def create_inventory():
    return ProductInventory(
        product_name=fake.word(),
        product_number=randint(1000, 9999),
        product_quantity=randint(1, 100),
        product_price=randint(1, 100)
    )

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Create users with unique usernames
        users = []
        
        # Append a unique number to the username
        for i in range(20):
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

        # Create inventory
        for user in users:
            products = [create_inventory() for _ in range(10)]
            for product in products:
                product.user_id = user.id
            db.session.add_all(products)

        db.session.commit()

    print("Seed completed successfully.")
