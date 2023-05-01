from pymongo import MongoClient

def recommend_products(customer_history, num_recommendations):
    client = MongoClient()
    db = client['mydatabase']
    inventory = db['inventory']

    # Sum up the number of times each product has been purchased
    product_counts = {}
    for product in inventory.find():
        product_counts[product['productName']] = product['added_count']

    # Sort products by popularity
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)

    # Recommend the most popular products that the customer hasn't already purchased
    recommendations = []
    for product, count in sorted_products:
        if product not in customer_history:
            recommendations.append(product)
            if len(recommendations) == num_recommendations:
                break

    return recommendations
