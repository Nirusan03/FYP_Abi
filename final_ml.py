import random
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from pymongo import *

cluster = MongoClient("mongodb://localhost:27017")
db_storage = cluster["Storage"]
collection_products = db_storage["Inventory"]
retrieve_customer_product = collection_products.find()
customer_products = []
product_list = []

for data in retrieve_customer_product:
    product_list.append(data)

# One-hot encode the categorical variables
categories = set(p["category"] for p in product_list)
vendors = set(p["vendor"] for p in product_list)
enc = OneHotEncoder(categories=[list(categories), list(vendors)])
X_cat = [[p["category"], p["vendor"]] for p in product_list]
X_cat_enc = enc.fit_transform(X_cat).toarray()

# Combine the one-hot encoded categorical variables with the numerical variables
X_num = [[p["added_count"]] for p in product_list]
X = np.hstack([X_cat_enc, X_num])

# Create the k-NN model
n_neighbors = 3
knn = NearestNeighbors(n_neighbors=n_neighbors)

# Fit the model to the data
knn.fit(X)

# Choose a random product as the query
query_index = random.randint(0, len(product_list) - 1)
query = X[query_index]

# Find the k nearest neighbors to the query
distances, indices = knn.kneighbors([query])

# Get the suggested products
suggested_products = []
for index in indices[0]:
    p = product_list[index]
    suggested_products.append(p)

# Print the suggested products
print("Suggested products:")
for p in suggested_products:
    print(p)
