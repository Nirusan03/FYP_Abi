import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")
database = cluster["Storage"]
collection = database["Inventory"]

# Collection is like a mini database inside the cluster
# Each collection something known as post. Post means entries

deletingManyDate = collection.delete_many({})
post = {"_id": 0,
        "quantity": 400,
        "productId": 1,
        "productName": "Soap",
        "price": 200,
        "vendor": "Vendor1"}

post1 = {"_id": 1,
         "quantity": 400,
         "productId": 2,
         "productName": "Brush",
         "price": 400,
         "vendor": "Vendor2"}

post2 = {"_id": 2,
         "quantity": 800,
         "productId": 3,
         "productName": "Mask",
         "price": 10,
         "vendor": "Vendor1"}

post3 = {"_id": 3,
         "quantity": 100,
         "productId": 4,
         "productName": "Sanitizers",
         "price": 300,
         "vendor": "Vendor2"}

post4 = {"_id": 4,
         "quantity": 100,
         "productId": 5,
         "productName": "Sanitizers",
         "price": 300,
         "vendor": "Vendor1"}

post5 = {"_id": 5,
         "quantity": 50,
         "productId": 6,
         "productName": "Condoms",
         "price": 2.99,
         "vendor": "Vendor2"}

post6 = {"_id": 6,
         "quantity": 20,
         "productId": 7,
         "productName": "Medicines",
         "price": 10,
         "vendor": "Vendor1"}

post7 = {"_id": 7,
         "quantity": 20,
         "productId": 8,
         "productName": "Mac",
         "price": 20,
         "vendor": "Vendor1"}
# Inserting single line
# collection.insert_one(post)

# Inserting multiple lines
collection.insert_many([post1, post2, post3, post4, post5, post6, post7])

# Finding data in database
results = collection.find({"_id": 3})
# print(type(results))

for result in results:
    # Results is a "pymongo" class object.
    # When looping through the mongo object using random element.
    # The element will be assigned as DICTIONARY
    # Printing the value of selected key in the dictionary
    print(result["_id"])
    # print(type(results))

# Sort the documents based on a specific field in ascending order
sorted_cursor = collection.find().sort('productName', 1)

# Create an empty list to store the sorted documents
sorted_docs = []

# Iterate over the sorted cursor and append each document to the list
for doc in sorted_cursor:
    sorted_docs.append(doc)

# Delete all existing documents from the collection
collection.delete_many({})

# Insert the sorted documents back into the collection
collection.insert_many(sorted_docs)
# # Finding one data in database
# results1 = collection.find_one({"name": "Nirusan"})
# print(results1)

# # When we just mention find all data will be shown
# showAll = collection.find({})
# for entry in showAll:
#     print(entry)
#
# # Deleting one document
# deletingDate = collection.delete_one({"_id" : 0})
#
# # Deleting many document
# deletingManyDate = collection.delete_many({})
#
# insertData = collection.insert_many([post, post1, post2])
#
# updateData = collection.update_one({"_id" : 0}, {"$set": {"name": "Shans"}})
#
# # If the given entries key value is new then data will be added as new
# updateData2 = collection.update_one({"_id" : 0}, {"$set": {"age": 21}})
#
# # Incrementing a value
# increment = collection.update_one({"_id" : 0}, {"$inc": {"age": 1}})
#
# post_count = collection.count_documents({})
# print(post_count)

# key = "Interest_Code"
# result2 = collection2.distinct("Interest_Code")
# for i in result2:
#     print(i)
