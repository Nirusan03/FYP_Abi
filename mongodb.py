import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")
database = cluster["Storage"]
collection = database["Inventory"]

deletingManyDate = collection.delete_many({})
post = {"_id": 0,
        "quantity": 400,
        "productId": 0,
        "productName": "Soap",
        "price": 200,
        "category": "Personal Protective Equipment (PPE)",
        "vendor": "Vendor1",
        "added_count": 20}

post1 = {"_id": 1,
         "quantity": 400,
         "productId": 1,
         "productName": "Brush",
         "price": 400,
         "category": "Surgical Supplies",
         "vendor": "Vendor2",
         "added_count": 10}

post2 = {"_id": 2,
         "quantity": 800,
         "productId": 2,
         "productName": "Mask",
         "price": 10,
         "category": "Laboratory Supplies",
         "vendor": "Vendor1",
         "added_count": 15}

post3 = {"_id": 3,
         "quantity": 100,
         "productId": 3,
         "productName": "Sanitizers",
         "price": 300,
         "category": "Sterile instruments",
         "vendor": "Vendor2",
         "added_count": 2}

post4 = {"_id": 4,
         "quantity": 100,
         "productId": 4,
         "productName": "Sanitizers",
         "price": 300,
         "category": "Pharmaceuticals",
         "vendor": "Vendor1",
         "added_count": 1}

post5 = {"_id": 5,
         "quantity": 50,
         "productId": 5,
         "productName": "Condoms",
         "price": 2.99,
         "category": "Diagnostic Equipment",
         "vendor": "Vendor2",
         "added_count": 6}

post6 = {"_id": 6,
         "quantity": 20,
         "productId": 6,
         "productName": "Medicines",
         "price": 10,
         "category": "Wound Care Supplies",
         "vendor": "Vendor1",
         "added_count": 7}

post7 = {"_id": 7,
         "quantity": 20,
         "productId": 7,
         "productName": "Mac",
         "price": 20,
         "category": "Laboratory Supplies",
         "vendor": "Vendor1",
         "added_count": 8}

# Inserting multiple lines
collection.insert_many([post1, post2, post3, post4, post5, post6, post7])

sorted_cursor = collection.find().sort('productName', 1)

sorted_docs = []

for doc in sorted_cursor:
    sorted_docs.append(doc)

collection.delete_many({})

collection.insert_many(sorted_docs)

