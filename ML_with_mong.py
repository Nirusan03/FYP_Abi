import pymongo
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# Connect to MongoDB and load data into a pandas dataframe
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['product_data']
data = list(collection.find({}, {'_id':0}))
df = pd.DataFrame(data)

# Scale the numerical features
scaler = MinMaxScaler()
numerical_features = ['product_price', 'product_bought_times']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Train the k-nearest neighbors model
k = 5  # number of similar products to recommend
model = NearestNeighbors(n_neighbors=k, algorithm='ball_tree')
model.fit(df[numerical_features])

# Create a function to recommend products
def recommend_products(product_id):
    product = df.loc[df['product_id'] == product_id]
    product_features = product[numerical_features]
    distances, indices = model.kneighbors(product_features)
    similar_product_indices = indices.flatten()[1:]  # exclude the current product
    similar_products = df.loc[similar_product_indices]
    recommended_products = list(similar_products['product_name'])
    return recommended_products

# Test the recommendation function for a sample product ID
product_id = 2
recommended_products = recommend_products(product_id)
print(f"Recommended products for product ID {product_id}: {recommended_products}")
