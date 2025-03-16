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

2.