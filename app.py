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
customer = ""
vendor = ""
retrieve_orders = collection.find()
upcoming_order = []
cluster_name_prefix = ""
cluster_name_prefix_vendor = ""

for documents in retrieve_orders:
    upcoming_order.append(documents)


# CUSTOMER
@app.route('/')
def signup_vendor():
    return render_template('signup-vendor.html')


@app.route('/signup_vendor2')
def signup_vendor2():
    return render_template('signup-vendor2.html')


@app.route('/signup_vendor3')
def signup_vendor3():
    return render_template('signup-vendor3.html')


@app.route('/signup_customer')
def signup_customer():
    return render_template('signup-vendor.html')


@app.route('/signup_customer2')
def signup_customer2():
    return render_template('signup-customer2.html')


@app.route('/signup_customer3')
def signup_customer3():
    return render_template('signup-customer3.html')


@app.route('/create_clusters_customer', methods=['POST'])
def create_clusters_customer():
    global cluster_name_prefix
    # Get the form data
    cluster_name_prefix = request.form['cluster_name_prefix']
    cluster_number = request.form['cluster_number']
    cluster_email = request.form['cluster_email']
    cluster_password = request.form['cluster_password']
    # Create the clusters
    for i in range(1):
        cluster_name = f"{cluster_name_prefix}"
        create_cluster_customer(cluster_name, cluster_number, cluster_email, cluster_password)

    # Return a success message
    return redirect(url_for('signup_customer2'))


def create_cluster_customer(cluster_name, cluster_number, cluster_email, cluster_password):
    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    db = client.test
    temp_database = client["test"]
    # Create the new cluster
    db.create_collection(cluster_name)
    temp_collection = temp_database[cluster_name]

    post = {
        "Customer_name": cluster_name,
        "Customer_email": cluster_email,
        "Customer_PhoneNo": cluster_number,
        "Customer_Password": cluster_password
    }
    temp_collection.insert_one(post)


@app.route('/insert_signup_customer2', methods=['POST'])
def insert_signup_customer2():
    global cluster_name_prefix
    # Get the form data
    cluster_company = request.form['cluster_company']
    cluster_address = request.form['cluster_address']
    cluster_tax_no = request.form['cluster_taxNo']
    cluster_shipping = request.form['cluster_shipping']
    cluster_business = request.form['cluster_business']

    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    temp_database = client["test"]
    temp_collection = temp_database[cluster_name_prefix]

    post = {
        "Customer_company": cluster_company,
        "Customer_ComAddress": cluster_address,
        "Customer_TaxNo": cluster_tax_no,
        "Customer_Shipping": cluster_shipping,
        "Customer_business": cluster_business
    }
    temp_collection.update_one({"Customer_name": cluster_name_prefix}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_customer3'))


@app.route('/insert_signup_customer2', methods=['POST'])
def insert_signup_customer2():
    global cluster_name_prefix
    # Get the form data
    cluster_payment_term = request.form['cluster_paymentTerm']
    cluster_name_card = request.form['cluster_nameCard']
    cluster_card_no = request.form['cluster_cardNo']
    cluster_card_ex = request.form['cluster_cardEx']
    cluster_cvc = request.form['cluster_cvc']

    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    db = client.test
    temp_database = client["test"]
    temp_collection = temp_database[cluster_name_prefix]

    post = {
        "Customer_Payment_Term": cluster_payment_term,
        "Customer_NameCard": cluster_name_card,
        "Customer_cardNo": cluster_card_no,
        "Customer_cardEx": cluster_card_ex,
        "Customer_cvc": cluster_cvc
    }
    temp_collection.update_one({"Customer_name": cluster_name_prefix}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('home_customer', cluster_name=f"{cluster_name_prefix}"))


@app.route('/login_page_customer')
def login_page_customer():
    return render_template('login-customer.html')


@app.route('/login_customer', methods=['POST'])
def login_customer():
    global customer
    # Get the username and password from the form
    username = request.form['username']
    # Check if the collection is available in the database
    if username in db.list_collection_names():
        customer = username
        return redirect(url_for('home_customer', cluster_name=customer))
    else:
        return redirect(url_for('login_page_customer'))


@app.route('/home_customer/<cluster_name>')
def home_customer(cluster_name):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer.html', date=date, upcoming_orders=upcoming_order, cluster_name=cluster_name)


@app.route('/create_clusters_vendor', methods=['POST'])
def create_clusters_vendor():
    global cluster_name_prefix_vendor
    # Get the form data
    cluster_name_prefix_vendor = request.form['cluster_name_prefix']
    cluster_code = request.form['cluster_code']
    cluster_phone_no = request.form['cluster_phoneNo']
    cluster_address = request.form['cluster_address']
    cluster_email = request.form['cluster_email']
    cluster_password = request.form['cluster_password']

    # Create the clusters
    for i in range(1):
        cluster_name = f"{cluster_name_prefix_vendor}"
        create_cluster_vendor(cluster_name, cluster_code, cluster_phone_no,
                              cluster_address, cluster_email, cluster_password)

    # Return a success message
    # return redirect(url_for('customer', cluster_name=f"{cluster_name_prefix}"))
    return redirect(url_for('signup_vendor2'))


def create_cluster_vendor(cluster_name, cluster_code, cluster_phone_no, cluster_address, cluster_email,
                          cluster_password):
    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    db = client.test
    temp_database = client["test"]
    # Create the new cluster
    db.create_collection(cluster_name)
    temp_collection = temp_database[cluster_name]

    post = {
        "Vendor_name": cluster_name,
        "Vendor_Code": cluster_code,
        "Vendor_phoneNo": cluster_phone_no,
        "Vendor_Address": cluster_address,
        "Vendor_email": cluster_email,
        "Vendor_Password": cluster_password
    }
    temp_collection.insert_one(post)


@app.route('/insert_signup_vendor', methods=['POST'])
def insert_signup_vendor():
    # Get the form data
    cluster_registration_no = request.form['cluster_registrationNo']
    cluster_vat = request.form['cluster_vat']
    cluster_registration = request.form['cluster_registration']
    cluster_regis_cert = request.form['cluster_regisCert']
    cluster_product_cert = request.form['cluster_productCert']

    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    temp_database = client["test"]
    temp_collection = temp_database[cluster_name_prefix]

    post = {
        "Vendor_RegisterNo": cluster_registration_no,
        "Vendor_vat": cluster_vat,
        "Vendor_Registration": cluster_registration,
        "Vendor_regisCert": cluster_regis_cert,
        "Vendor_productCert": cluster_product_cert
    }
    temp_collection.update_one({"Vendor_name": cluster_name_prefix_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_vendor3'))


@app.route('/insert_signup_vendor3', methods=['POST'])
def insert_signup_vendor3():
    global cluster_name_prefix
    # Get the form data
    cluster_bank_name = request.form['cluster_bankName']
    cluster_bank_add = request.form['cluster_bankAdd']
    cluster_acc_name = request.form['cluster_accName']
    cluster_acc_no = request.form['cluster_accNo']
    cluster_statement = request.form['cluster_statement']

    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Get the "test" database
    temp_database = client["test"]
    temp_collection = temp_database[cluster_name_prefix]

    post = {
        "Vendor_bankName": cluster_bank_name,
        "Vendor_bankAddress": cluster_bank_add,
        "Vendor_AccName": cluster_acc_name,
        "Vendor_AccNo": cluster_acc_no,
        "Vendor_statement": cluster_statement
    }
    temp_collection.update_one({"Vendor_name": cluster_name_prefix_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('home_vendor', cluster_name=f"{cluster_name_prefix_vendor}"))


@app.route('/login_page_vendor')
def login_page_vendor():
    return render_template('login-vendor.html')


@app.route('/login_vendor', methods=['POST'])
def login_vendor():
    global vendor
    # Get the username and password from the form
    username = request.form['username']
    # Check if the collection is available in the database
    if username in db.list_collection_names():
        vendor = username
        return redirect(url_for('home_vendor', cluster_name=vendor))
    else:
        return redirect(url_for('login_page_vendor'))


@app.route('/home_vendor/<cluster_name>')
def home_vendor(cluster_name):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor.html', date=date, upcoming_orders=upcoming_order, cluster_name=cluster_name)


@app.route('/products')
def products():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('products.html', date=date, upcoming_orders=upcoming_order, customer=customer)


@app.route('/inventory')
def inventory():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('inventory.html', date=date, upcoming_orders=upcoming_order, vendor=vendor)


@app.route('/insert_data', methods=['POST'])
def insert_data():
    button_value = request.form['my-button']
    words = [w.strip() for w in button_value.split()]
    vendor_here = "Vendor" + words[1]
    print(vendor_here + " :  user name ")
    print(button_value)
    collection2 = db[vendor_here]
    collection2.insert_one({'data': button_value})
    return 'Data inserted successfully!'


@app.route('/rfq_vendor')
def rfq_vendor():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('rfq-vendor.html', date=date, upcoming_orders=upcoming_order)


if __name__ == "__main__":
    app.run(debug=True)
