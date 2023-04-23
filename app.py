from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import datetime
from pymongo import *

app = Flask(__name__)
cluster = MongoClient("mongodb://localhost:27017")
database = cluster["Fyp_Abi"]
collection = database["vendor"]
db = cluster['test']

retrieve_orders = collection.find()
upcoming_order = []

for documents in retrieve_orders:
    upcoming_order.append(documents)


@app.route('/')
def signup():
    return render_template('signup-vendor.html')


@app.route('/create_clusters', methods=['POST'])
def create_clusters():
    # Get the form data
    cluster_name_prefix = request.form['cluster_name_prefix']

    # Create the clusters
    for i in range(1):
        cluster_name = f"{cluster_name_prefix}"
        create_cluster(cluster_name)

    # Return a success message
    return redirect(url_for('home_vendor', cluster_name=f"{cluster_name_prefix}"))


def create_cluster(cluster_name):
    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    db = client.test

    # Create the new cluster
    db.create_collection(cluster_name)


@app.route('/login_page')
def login_page():
    return render_template('login-vendor.html')


@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the form
    username = request.form['username']

    # Check if the collection is available in the database
    if username in db.list_collection_names():
        return redirect(url_for('home_vendor', cluster_name=username))
    else:
        return redirect(url_for('login_page'))


@app.route('/home_vendor/<cluster_name>')
def home_vendor(cluster_name):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor.html', date=date, upcoming_orders=upcoming_order, cluster_name=cluster_name)


@app.route('/customer')
def customer():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer.html', date=date, upcoming_orders=upcoming_order)


if __name__ == "__main__":
    app.run(debug=True)