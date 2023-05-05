import random
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import numpy as np

product_list = [
    {"_id": 0, "quantity": 400, "productId": 0, "productName": "Soap", "price": 200, "category": "Personal Protective Equipment (PPE)", "vendor": "Vendor1", "added_count": 20},
    {"_id": 1, "quantity": 400, "productId": 1, "productName": "Brush", "price": 400, "category": "Surgical Supplies", "vendor": "Vendor2", "added_count": 10},
    {"_id": 2, "quantity": 800, "productId": 2, "productName": "Mask", "price": 10, "category": "Laboratory Supplies", "vendor": "Vendor1", "added_count": 15},
    {"_id": 3, "quantity": 100, "productId": 3, "productName": "Sanitizers", "price": 300, "category": "Sterile instruments", "vendor": "Vendor2", "added_count": 2},
    {"_id": 4, "quantity": 100, "productId": 4, "productName": "Sanitizers", "price": 300, "category": "Pharmaceuticals", "vendor": "Vendor1", "added_count": 1},
    {"_id": 5, "quantity": 50, "productId": 5, "productName": "Condoms", "price": 2.99, "category": "Diagnostic Equipment", "vendor": "Vendor2", "added_count": 6},
    {"_id": 6, "quantity": 20, "productId": 6, "productName": "Medicines", "price": 10, "category": "Wound Care Supplies", "vendor": "Vendor1", "added_count": 7},
    {"_id": 7, "quantity": 20, "productId": 7, "productName": "Mac", "price": 20, "category": "Laboratory Supplies", "vendor": "Vendor1", "added_count": 8}
]

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
print(type(suggested_products))
for p in suggested_products:
    print(p)
    # print(p["productName"], p["category"], p["added_count"])

# Append the suggested products to a new list and show it to the user
new_products = []
for p in suggested_products:
    new_products.append(p)

print("New products:")
for p in new_products:
    print("- {} (category: {}, added_count: {})".format(p["productName"], p["category"], p["added_count"]))

