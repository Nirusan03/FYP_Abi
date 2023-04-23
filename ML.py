import numpy as np

# Define a list of items and their features
items = [
    {"name": "apple", "color": "red", "taste": "sweet", "price": 0.5},
    {"name": "banana", "color": "yellow", "taste": "sweet", "price": 0.25},
    {"name": "orange", "color": "orange", "taste": "tart", "price": 0.75},
    {"name": "pear", "color": "green", "taste": "sweet", "price": 0.6},
    {"name": "grape", "color": "purple", "taste": "sweet", "price": 1.2},
]


# Define a function that uses machine learning to suggest an item from the list based on the user's preferences
def suggest_item(preferences):
    # Convert the list of items into a matrix
    item_matrix = np.array([[item["color"], item["taste"], item["price"]] for item in items])

    # Convert the user's preferences into a vector
    preference_vector = np.array(preferences)

    # Calculate the similarity between the user's preferences and each item
    similarity_scores = np.dot(item_matrix, preference_vector)

    # Sort the items by their similarity score and return the most similar item
    most_similar_item_index = np.argmax(similarity_scores)
    suggested_item = items[most_similar_item_index]["name"]

    return suggested_item


# Ask the user for their preferences
color_preference = input("What color do you prefer? (red, yellow, orange, green, purple): ")
taste_preference = input("What taste do you prefer? (sweet, tart): ")
price_preference = float(input("What is your budget? (in dollars): "))

# Normalize the user's preferences
preference_vector = [color_preference, taste_preference, price_preference]
preference_vector = [1 if v == "sweet" else -1 if v == "tart" else v for v in preference_vector]
preference_vector[2] = (preference_vector[2] - 0.25) / 1.2

# Call the suggest_item() function to get a recommendation and print the suggested item
suggested_item = suggest_item(preference_vector)
print("Based on your preferences, we suggest trying", suggested_item, ".")
