import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")
database = cluster["Fyp_Abi"]
collection = database["vendor"]

# Collection is like a mini database inside the cluster
# Each collection something known as post. Post means entries

deletingManyDate = collection.delete_many({})
post = {"_id": 1,
        "quantity": 400,
        "productId": 1,
        "productName": "Soap",
        "price": 200,
        "vendor": 1}

post1 = {"_id": 2,
         "quantity": 400,
         "productId": 2,
         "productName": "Brush",
         "price": 400,
         "vendor": 2}

post2 = {"_id": 3,
         "quantity": 800,
         "productId": 3,
         "productName": "Mask",
         "price": 10,
         "vendor": 1}

post3 = {"_id": 4,
         "quantity": 100,
         "productId": 4,
         "productName": "Sanitizers",
         "price": 300,
         "vendor": 2}

post4 = {"_id": 5,
         "quantity": 100,
         "productId": 5,
         "productName": "Sanitizers",
         "price": 300,
         "vendor": 1}

post5 = {"_id": 6,
         "quantity": 50,
         "productId": 6,
         "productName": "Condoms",
         "price": 2.99,
         "vendor": 2}

post6 = {"_id": 7,
         "quantity": 20,
         "productId": 7,
         "productName": "Medicines",
         "price": 10,
         "vendor": 1}
# Inserting single line
# collection.insert_one(post)

# Inserting multiple lines
collection.insert_many([post1, post2, post3, post4, post5, post6])

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
