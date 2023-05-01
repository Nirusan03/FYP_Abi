import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import *

# Define the MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['Storage']
collection = db['Inventory']

# Define the product dictionary
product_dict = {
    "Product A": {
        "productId": 1,
        "price": 100,
        "added_count": 10,
        "category": "Category A"
    },
    "Product B": {
        "productId": 2,
        "price": 200,
        "added_count": 20,
        "category": "Category A"
    },
    "Product C": {
        "productId": 3,
        "price": 150,
        "added_count": 15,
        "category": "Category B"
    },
    "Product D": {
        "productId": 4,
        "price": 300,
        "added_count": 25,
        "category": "Category B"
    }
}

# Convert the product dictionary to a pandas dataframe
df = pd.DataFrame.from_dict(product_dict, orient='index')
df['productFeatures'] = df['category'] + ' ' + df['added_count'].astype(str) + ' ' + df['price'].astype(str)

# Create a TfidfVectorizer object and fit it on the product features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['productFeatures'])

# Define a function to recommend products
def recommend_products(purchase_history):
    # Convert the purchase history to a pandas dataframe
    purchase_df = pd.DataFrame.from_dict(purchase_history, orient='index', columns=['quantity'])
    purchase_df.index.name = 'productName'
    
    # Join the purchase history dataframe with the product dataframe
    joined_df = purchase_df.join(df, on='productName')
    
    # Compute the tf-idf matrix for the purchased products
    purchase_matrix = vectorizer.transform(joined_df['productFeatures'])
    
    # Compute the cosine similarity between the purchased products and all other products
    similarity_scores = cosine_similarity(purchase_matrix, X)
    
    # Find the indices of the most similar products
    similar_indices = similarity_scores.argsort()[:, ::-1][0][:10]
    
    # Get the names of the recommended products
    recommended_products = list(df.iloc[similar_indices].index)
    
    return recommended_products

# Test the recommendation function
purchase_history = {
    "Product A": 2,
    "Product C": 1
}
recommended_products = recommend_products(purchase_history)
print(f"Recommended products: {recommended_products}")
