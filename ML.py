import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# load data into a pandas dataframe
data = {
    "product_name": ["Product A", "Product B", "Product C", "Product D"],
    "product_id": [1, 2, 3, 4],
    "product_price": [100, 200, 150, 300],
    "product_bought_times": [10, 20, 15, 25],
}
df = pd.DataFrame(data)

# feature engineering: create new features if needed
# for example, you can create a feature called "price_per_bought_time"

# define features and target variable
X = df[["product_price", "product_bought_times"]]
y = df["product_name"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# train a random forest classifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# evaluate the model on the testing set
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# use the trained model to make predictions for new data
new_data = {
    "product_price": [250],
    "product_bought_times": [5],
}
X_new = pd.DataFrame(new_data)
y_pred_new = clf.predict(X_new)
print(f"Recommended product: {y_pred_new}")
