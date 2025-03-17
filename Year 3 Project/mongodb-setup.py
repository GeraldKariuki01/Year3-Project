# MongoDB Setup
# For djongo to work with MongoDB, we need to install the required packages
# pip install djongo pymongo

# MongoDB Schema Design
'''
MongoDB Collections:

1. users
{
    "_id": ObjectId,
    "username": String,
    "email": String,
    "password": String (hashed),
    "first_name": String,
    "last_name": String,
    "user_type": String (enum: ["farmer", "buyer"]),
    "phone_number": String,
    "address": String,
    "profile_image": String (URL),
    "date_joined": Date,
    "is_active": Boolean
}

2. products
{
    "_id": ObjectId,
    "title": String,
    "description": String,
    "price": Decimal,
    "image_url": String (URL),
    "category": String (enum: ["vegetables", "fruits", "grains", "dairy", "other"]),
    "farmer_id": ObjectId (reference to users),
    "location": String,
    "harvest_date": Date,
    "is_organic": Boolean,
    "quantity": Integer,
    "created_at": Date,
    "updated_at": Date
}

3. orders
{
    "_id": ObjectId,
    "buyer_id": ObjectId (reference to users),
    "items": [
        {
            "product_id": ObjectId (reference to products),
            "quantity": Integer,
            "price": Decimal
        }
    ],
    "total_amount": Decimal,
    "shipping_address": String,
    "phone_number": String,
    "status": String (enum: ["pending", "processing", "shipped", "delivered", "cancelled"]),
    "created_at": Date,
    "updated_at": Date
}

4. reviews
{
    "_id": ObjectId,
    "product_id": ObjectId (reference to products),
    "user_id": ObjectId (reference to users),
    "rating": Integer (1-5),
    "comment": String,
    "created_at": Date
}
'''

# MongoDB Initial Setup Script
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
import json
from bson import ObjectId
from datetime import datetime, timedelta

def setup_mongodb():
    """
    Initialize MongoDB database with collections and indexes
    """
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        
        # Create or access the database
        db = client['agriconnect_db']
        
        # Create collections if they don't exist
        if 'users' not in db.list_collection_names():
            users = db.create_collection('users')
            # Create indexes for users collection
            users.create_index('username', unique=True)
            users.create_index('email', unique=True)
            print("Users collection created with indexes")
        
        if 'products' not in db.list_collection_names():
            products = db.create_collection('products')
            # Create indexes for products collection
            products.create_index('farmer_id')
            products.create_index('category')
            products.create_index([('title', 'text'), ('description', 'text')])
            print("Products collection created with indexes")
        
        if 'orders' not in db.list_collection_names():
            orders = db.create_collection('orders')
            # Create indexes for orders collection
            orders.create_index('buyer_id')
            orders.create_index('status')
            orders.create_index('created_at')
            print("Orders collection created with indexes")
        
        if 'reviews' not in db.list_collection_names():
            reviews = db.create_collection('reviews')
            # Create indexes for reviews collection
            reviews.create_index([('product_id', 1), ('user_id', 1)], unique=True)
            reviews.create_index('product_id')
            print("Reviews collection created with indexes")
        
        print("MongoDB setup completed successfully")
        return True
        
    except ServerSelectionTimeoutError:
        print("MongoDB connection failed. Make sure MongoDB server is running.")
        return False
    except Exception as e:
        print(f"Error setting up MongoDB: {str(e)}")
        return False

def seed_demo_data():
    """
    Seed the database with demo data for testing
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['agriconnect_db']
        
        # Only seed if collections are empty
        if db.users.count_documents({}) == 0:
            # Create demo farmers
            farmers = [
                {
                    "username": "farmer1",
                    "email": "farmer1@example.com",
                    "password": "pbkdf2_sha256$260000$randomhash123$somehashedpassword",  # In production, use proper hashing
                    "first_name": "John",
                    "last_name": "Doe",
                    "user_type": "farmer",
                    "phone_number": "+1234567890",
                    "address": "Farm Road 123, Rural Area",
                    "profile_image": "https://randomuser.me/api/portraits/men/1.jpg",
                    "date_joined": datetime.now(),
                    "is_active": True
                },
                {
                    "username": "farmer2",
                    "email": "farmer2@example.com",
                    "password": "pbkdf2_sha256$260000$randomhash456$somehashedpassword",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "user_type": "farmer",
                    "phone_number": "+1987654321",
                    "address": "Village Lane 456, Countryside",
                    "profile_image": "https://randomuser.me/api/portraits/women/1.jpg",
                    "date_joined": datetime.now(),
                    "is_active": True
                }
            ]
            
            farmer_ids = []
            for farmer in farmers:
                result = db.users.insert_one(farmer)
                farmer_ids.append(result.inserted_id)
            
            # Create demo buyers
            buyers = [
                {
                    "username": "buyer1",
                    "email": "buyer1@example.com",
                    "password": "pbkdf2_sha256$260000$randomhash789$somehashedpassword",
                    "first_name": "Michael",
                    "last_name": "Johnson",
                    "user_type": "buyer",
                    "phone_number": "+1122334455",
                    "address": "123 Main St, City",
                    "profile_image": "https://randomuser.me/api/portraits/men/2.jpg",
                    "date_joined": datetime.now(),
                    "is_active": True
                }
            ]
            
            buyer_ids = []
            for buyer in buyers:
                result = db.users.insert_one(buyer)
                buyer_ids.append(result.inserted_id)
            
            # Create demo products
            products = [
                {
                    "title": "Fresh Organic Tomatoes",
                    "description": "Locally grown organic tomatoes, perfect for salads and cooking.",
                    "price": 2.99,
                    "image_url": "https://images.unsplash.com/photo-1592924357228-9b5bb8e0f27f",
                    "category": "vegetables",
                    "farmer_id": farmer_ids[0],
                    "location": "Rural Area, State",
                    "harvest_date": datetime.now() - timedelta(days=2),
                    "is_organic": True,
                    "quantity": 100,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                },
                {
                    "title": "Farm Fresh Eggs",
                    "description": "Free-range chicken eggs from our family farm.",
                    "price": 4.50,
                    "image_url": "https://images.unsplash.com/photo-1506976785307-8732e854ad03",
                    "category": "dairy",
                    "farmer_id": farmer_ids[0],
                    "location": "Rural Area, State",
                    "harvest_date": datetime.now() - timedelta(days=1),
                    "is_organic": True,
                    "quantity": 50,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                },
                {
                    "title": "Organic Apples",
                    "description": "Sweet and juicy apples from our orchard.",
                    "price": 1.99,
                    "image_url": "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce",
                    "category": "fruits",
                    "farmer_id": farmer_ids[1],
                    "location": "Countryside, State",
                    "harvest_date": datetime.now() - timedelta(days=3),
                    "is_organic": True,
                    "quantity": 200,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                },
                {
                    "title": "Brown Rice",
                    "description": "Naturally grown brown rice, rich in nutrients.",
                    "price": 3.25,
                    "image_url": "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6",
                    "category": "grains",
                    "farmer_id": farmer_ids[1],
                    "location": "Countryside, State",
                    "harvest_date": datetime.now() - timedelta(days=30),
                    "is_organic": False,
                    "quantity": 150,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            ]
            
            product_ids = []
            for product in products:
                result = db.products.insert_one(product)
                product_ids.append(result.inserted_id)
            
            # Create demo orders
            orders = [
                {
                    "buyer_id": buyer_ids[0],
                    "items": [
                        {
                            "product_id": product_ids[0],
                            "quantity": 5,
                            "price": 2.99
                        },
                        {
                            "product_id": product_ids[1],
                            "quantity": 2,
                            "price": 4.50
                        }
                    ],
                    "total_amount": 5 * 2.99 + 2 * 4.50,
                    "shipping_address": "123 Main St, City",
                    "phone_number": "+1122334455",
                    "status": "delivered",
                    "created_at": datetime.now() - timedelta(days=10),
                    "updated_at": datetime.now() - timedelta(days=7)
                },
                {
                    "buyer_id": buyer_ids[0],
                    "items": [
                        {
                            "product_id": product_ids[2],
                            "quantity": 10,
                            "price": 1.99
                        }
                    ],
                    "total_amount": 10 * 1.99,
                    "shipping_address": "123 Main St, City",
                    "phone_number": "+1122334455",
                    "status": "pending",
                    "created_at": datetime.now() - timedelta(hours=2),
                    "updated_at": datetime.now() - timedelta(hours=2)
                }
            ]
            
            order_ids = []
            for order in orders:
                result = db.orders.insert_one(order)
                order_ids.append(result.inserted_id)
            
            # Create demo reviews
            reviews = [
                {
                    "product_id": product_ids[0],
                    "user_id": buyer_ids[0],
                    "rating": 5,
                    "comment": "These tomatoes are amazing! Very fresh and flavorful.",
                    "created_at": datetime.now() - timedelta(days=5)
                },
                {
                    "product_id": product_ids[1],
                    "user_id": buyer_ids[0],
                    "rating": 4,
                    "comment": "Great eggs with rich yolks. Will buy again.",
                    "created_at": datetime.now() - timedelta(days=5)
                }
            ]
            
            for review in reviews:
                db.reviews.insert_one(review)
            
            print("Demo data seeded successfully")
            return True
            
    except Exception as e:
        print(f"Error seeding demo data: {str(e)}")
        return False

# MongoDB connection utility for the application
def get_db_connection():
    """
    Get a connection to the MongoDB database
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['agriconnect_db']
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        return None

# Commands to run setup and seeding
if __name__ == "__main__":
    print("Setting up MongoDB for AgriConnect...")
    if setup_mongodb():
        print("Would you like to seed the database with demo data? (y/n)")
        response = input().lower()
        if response == 'y':
            seed_demo_data()
