# Importing the required libraries

from flask import Flask, render_template, request, redirect, url_for  # To run flask server

from bson.objectid import ObjectId  # To detect the object id of the products

from pymongo import *  # To handle database

from itertools import groupby  # To group the item in mongoDB

import numpy as np  # To add products to vectors for machine learning
from sklearn.neighbors import NearestNeighbors  # For machine learning part - KNN
from sklearn.preprocessing import OneHotEncoder

from datetime import date, timedelta  # To show time and date
import datetime

import random  # To selected all the products in random sort and selecting the data

# Creating Flask object
app = Flask(__name__)

# Creating the object to connect python and mongodb
cluster = MongoClient("mongodb://localhost:27017")

# Connection of storage database in mongoDB
db_storage = cluster["Storage"]

# Connecting the inventory collection of inventory in the storage db
collection_products = db_storage["Inventory"]

# Connecting the vendor database
db_vendor = cluster['Vendor']

# Connecting the customer database
db_customer = cluster['Customer']

# Connecting both account database in customer, vendor to store user information
account_vendor_collection = db_vendor["Accounts"]
account_customer_collection = db_customer["Accounts"]

# Global variable to store customer, vendor name
customer = ""
vendor = ""

# Dictionary to find the single vendor's inventory details
retrieve_vendor_inventory = {}
vendor_inventory = []  # List to store the single vendor's inventory details

# Finding all inventory product, storing inside the dictionary
retrieve_customer_product = collection_products.find()
customer_products = []  # List to store the dictionary data separately

# To store cart details
carts = []

# Temp variable to store vendor, customer name
collection_vendor = ""
collection_customer = ""

# Temp variable to pass the data from product list to request for quote
product_name = ""
product_price = ""
product_quantity = ""
product_vendor = ""
product_customer = ""
product_id = 0
category = ""

# Appending vendor_inventory list to store Database data
for data in retrieve_vendor_inventory:
    vendor_inventory.append(data)

# Appending customer_products list to store Database data
for data in retrieve_customer_product:
    customer_products.append(data)


# Home route of the html page - Sign up page of vendor
@app.route('/')
def signup_vendor():
    return render_template('signup-vendor.html')


# Route for second sign page of vendor - Organization details
@app.route('/signup_vendor2')
def signup_vendor2():
    return render_template('signup-vendor2.html')


# Route for third sign page of vendor - Project team details
@app.route('/signup_vendor3')
def signup_vendor3():
    return render_template('signup-vendor3.html')


# Route for forth sign page of vendor - Technical details
@app.route('/signup_vendor4')
def signup_vendor4():
    return render_template('signup-vendor4.html')


# Route for fifth sign page of vendor - Payment details
@app.route('/signup_vendor5')
def signup_vendor5():
    return render_template('signup-vendor5.html')


# Route for sixth (final ) sign page of vendor - Verification
@app.route('/signup_vendor6')
def signup_vendor6():
    return render_template('signup-vendor6.html')


# Route for the firs sign page of customer -
@app.route('/signup_customer')
def signup_customer():
    return render_template('signup-customer.html')


# Route for second sign page of customer - Organization details
@app.route('/signup_customer2')
def signup_customer2():
    return render_template('signup-customer2.html')


# Route for third sign page of vendor - Payment details
@app.route('/signup_customer3')
def signup_customer3():
    return render_template('signup-customer3.html')


# Route for the admin page
@app.route('/admin_page')
def admin_page():
    """
        This admin_page function is for routing to the admin page and show the requests of
        vendors who are about to create accounts

        :return: admin.html page, argument: requesting vendor
    """

    # Accessing the global variables inside the local method
    global account_vendor_collection  # To update account collection in vendor

    # Getting the date and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Finding the collection data which has the value proceeding
    requesting_vendors = account_vendor_collection.find({"Vendor_request": "proceeding"})
    rv = []  # List to store the value proceeding documents

    # Appending the list
    for i in requesting_vendors:
        rv.append(i)

    return render_template('admin.html', date=date, rv=rv)


# The method which will get call when user enters admin click to check in admin_page
@app.route('/check_data', methods=['POST'])
def check_data():
    """
    Method to get the vendors data from button value and pass it

    :return: admin_request_vendor method, argument : vendor name
    """

    # Variable to store button value
    button_value = request.form['my-button']

    # Splitting the button values, storing them inside the list called word
    # Stripping the word to remove the additional spaces in the string value
    words = [w.strip() for w in button_value.split()]

    # Vendor name
    ven_name = words[0]

    # Returning to the admin_request_vendor method
    return redirect(url_for('admin_request_vendor', ven_name=ven_name))


# Routing method to call admin-request-vendor.html
@app.route('/admin_request_vendor/<ven_name>')
def admin_request_vendor(ven_name):
    """
    This method will find the particular of the vendor, who likes to create an
    account and pass it to the admin-request-vendor.html page
    :param ven_name:
    :return: admin-request-vendor.html, arguments : date, request vendor data dic
    """

    # Accessing the global variables inside the local method
    global account_vendor_collection  # To update account collection in vendor

    # Getting the date and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Finding the single vendor and storing inside the dictionary
    req_vend = account_vendor_collection.find_one({"Vendor_name": ven_name})

    # Returning to the html page
    return render_template('admin-request-vendor.html', date=date, req_vend=req_vend)


# Method will get call when vendor click verify button admin-request-vendor.html page
@app.route('/verify', methods=['POST'])
def verify():
    """
    A method to store and pass the verification digit that vendor passes
    :return: admin starting page
    """

    # Accessing the global variables inside the local method
    global account_vendor_collection, collection_vendor   # To update account collection in vendor, storing tem vendor

    # Reading the request digit that vendor entered inform
    ver_number = request.form['ver_number']

    # Variable to store button value
    button_values = request.form['my-button']

    # Splitting the button values, storing them inside the list called word
    # Stripping the word to remove the additional spaces in the string value
    words = [w.strip() for w in button_values.split()]

    # Vendor name
    vend_name = words[0]

    # Updating the vendors account collection by updating the verification digit
    account_vendor_collection.update_one({"Vendor_name": vend_name}, {"$set": {"request_dig": ver_number}},
                                         upsert=True)

    # Return to admin home page
    return render_template('admin.html')


# Routing to admin vendor page
@app.route('/admin_vendor_page')
def admin_vendor_page():
    """
    Function to route for admin-vendor page and show all the vendor details
    :return: admin-vendor.html, argument : date, vendor list
    """

    # Accessing the global variables inside the local method
    global account_vendor_collection  # vendor collection

    # Getting the date and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Fetching all the vendor data in dictionary
    all_vendor = account_vendor_collection.find({})
    vendors = []  # List to store vendor data

    # Appending the vendor list
    for document in all_vendor:
        vendors.append(document)

    # Returning the admin-vendor
    return render_template('admin-vendor.html', date=date, vendors=vendors)


# Routing to admin-customer.html
@app.route('/admin_customer_page')
def admin_customer_page():
    """
    Function to route for admin-customer page and show all the customer details
    :return: admin-customer.html, argument : date, customer list
    """

    # Accessing the global variables inside the local method
    global account_customer_collection  # customer collection

    # Getting the date and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Fetching all the customer data in dictionary
    all_customer = account_customer_collection.find({})
    customers = []  # List to store customer data

    # Appending the customers list
    for document in all_customer:
        customers.append(document)

    # Returning the admin-customer
    return render_template('admin-customer.html', date=date, customers=customers)


# Routing to admin-inventory.html
@app.route('/admin_inventory_page')
def admin_inventory_page():
    """
    Function to route for admin-inventory page and show all the inventory details
    :return: admin-inventory.html, argument : date, product list
    """

    # Accessing the global variables inside the local method
    global collection_products  # inventory collection

    # Getting the date and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Fetching all the product data in dictionary
    all_products = collection_products.find({})
    product = []  # List to store product data

    # Appending the product list
    for document in all_products:
        product.append(document)

    # Returning the admin-inventory.html
    return render_template('admin-inventory.html', date=date, product=product)


# Creating cluster for vendor
@app.route('/create_clusters_vendor', methods=['POST'])
def create_clusters_vendor():
    """
    Method to read input value from vendor sign up page and pas them to
    create_cluster_vendor method
    :return: signup_vendor2 method
    """

    # Accessing the global variables inside the local method
    global collection_vendor, vendor

    # Get the form data
    collection_vendor = request.form['cluster_vendor_name']  # Vendor name
    cluster_code = request.form['cluster_code']  # Vendor code
    cluster_phone_no = request.form['cluster_phoneNo']  # Vendor phone number
    cluster_address = request.form['cluster_address']  # Vendor address
    cluster_email = request.form['cluster_email']  # Vendor email
    cluster_password = request.form['cluster_password']   # Vendor password

    # Storing vendor name to global variable.
    vendor = collection_vendor
    # Create the clusters
    for i in range(1):
        collection_name = f"{collection_vendor}"

        # Calling the create_cluster_vendor method
        create_cluster_vendor(collection_name, cluster_code, cluster_phone_no,
                              cluster_address, cluster_email, cluster_password)

    # Returning signup_vendor2 method
    return redirect(url_for('signup_vendor2'))


# Method store insert data inside the mongodb
def create_cluster_vendor(collection_name, cluster_code, cluster_phone_no, cluster_address, cluster_email,
                          cluster_password):
    """
    A method to create a cluster for the vendor and pass them into
    :param collection_name:
    :param cluster_code:
    :param cluster_phone_no:
    :param cluster_address:
    :param cluster_email:
    :param cluster_password:
    :return:
    """
    global cluster, db_vendor

    # Create the new collection
    db_vendor.create_collection(collection_name)
    temp_collection = db_vendor[collection_name]

    post = {
        "Vendor_name": collection_name,
        "Vendor_Code": cluster_code,
        "Vendor_phoneNo": cluster_phone_no,
        "Vendor_Address": cluster_address,
        "Vendor_email": cluster_email,
        "Vendor_Password": cluster_password
    }
    account_vendor_collection.insert_one(post)


@app.route('/insert_signup_vendor2', methods=['POST'])
def insert_signup_vendor2():
    global collection_vendor, cluster, db_vendor

    # Get the form data
    cluster_registration_no = request.form['cluster_registrationNo']
    cluster_vat = request.form['cluster_vat']
    cluster_registration = request.form['cluster_registration']
    cluster_regis_cert = request.form['cluster_regisCert']
    cluster_product_cert = request.form['cluster_productCert']

    # Storing the data inside the dictionary
    post = {
        "Vendor_RegisterNo": cluster_registration_no,
        "Vendor_vat": cluster_vat,
        "Vendor_Registration": cluster_registration,
        "Vendor_regisCert": cluster_regis_cert,
        "Vendor_productCert": cluster_product_cert
    }

    # Upating the collection
    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_vendor3'))


@app.route('/insert_signup_vendor3', methods=['POST'])
def insert_signup_vendor3():
    global collection_vendor, cluster, db_vendor
    # Get the form data
    cluster_manager_name = request.form['cluster_manager_name']
    cluster_proj_leader = request.form['cluster_proj_leader']
    cluster_proj_contact = request.form['cluster_proj_contact']

    post = {
        "Vendor_manager": cluster_manager_name,
        "Vendor_project_leader": cluster_proj_leader,
        "Vendor_project_contact": cluster_proj_contact,
    }
    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_vendor4', cluster_name=f"{collection_vendor}"))


@app.route('/insert_signup_vendor4', methods=['POST'])
def insert_signup_vendor4():
    global collection_vendor, cluster, db_vendor
    # Get the form data
    cluster_tech_lead = request.form['cluster_tech_lead']
    cluster_tech_contact_no = request.form['cluster_tech_contact_no']
    cluster_tech_os = request.form['cluster_tech_os']

    post = {
        "Vendor_technical_leader": cluster_tech_lead,
        "Vendor_technical_contact_no": cluster_tech_contact_no,
        "Vendor_tech_os": cluster_tech_os,
    }
    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_vendor5', cluster_name=f"{collection_vendor}"))


@app.route('/insert_signup_vendor5', methods=['POST'])
def insert_signup_vendor5():
    global collection_vendor, cluster, db_vendor
    # Get the form data
    cluster_bank_name = request.form['cluster_bankName']
    cluster_bank_add = request.form['cluster_bankAdd']
    cluster_acc_name = request.form['cluster_accName']
    cluster_acc_no = request.form['cluster_accNo']
    cluster_statement = request.form['cluster_statement']

    post = {
        "Vendor_bankName": cluster_bank_name,
        "Vendor_bankAddress": cluster_bank_add,
        "Vendor_AccName": cluster_acc_name,
        "Vendor_AccNo": cluster_acc_no,
        "Vendor_statement": cluster_statement,
        "Vendor_request": "proceeding",
    }
    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_vendor6', cluster_name=f"{collection_vendor}"))


@app.route('/insert_signup_vendor6', methods=['POST'])
def insert_signup_vendor6():
    global collection_vendor, cluster, db_vendor, account_vendor_collection, db_vendor
    # Get the form data
    ver_number = int(request.form['ver_number'])

    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": {"Vendor_request": "proceeding"}},
                                         upsert=True)

    request_query = account_vendor_collection.find_one({"Vendor_name": collection_vendor})

    digit = int(request_query['request_dig'])
    print(digit, " the digit in database ", type(digit))
    print(ver_number, " the digit user entered ", type(ver_number))

    if ver_number == digit:
        account_vendor_collection.update_one({"Vendor_name": collection_vendor},
                                             {"$set": {"Vendor_request": "Accepted"}})
        # Return a success message
        return redirect(url_for('home_vendor', cluster_name=f"{collection_vendor}"))
    else:
        account_vendor_collection.delete_one({"Vendor_name": collection_vendor})
        collection = db_vendor[collection_vendor]
        collection.drop()
        return "Your registration got canceled"


@app.route('/login_page_vendor')
def login_page_vendor():
    return render_template('login-vendor.html')


@app.route('/login_vendor', methods=['POST'])
def login_vendor():
    global vendor
    # Get the vendor_name and password from the form
    vendor_name = request.form['vendor_name']
    # Check if the collection is available in the database
    if vendor_name in db_vendor.list_collection_names():
        vendor = vendor_name
        return redirect(url_for('home_vendor', cluster_name=vendor))
    else:
        return redirect(url_for('login_page_vendor'))

# Method to return for home
@app.route('/home_vendor/<cluster_name>')
def home_vendor(cluster_name):
    # accessing the global variables
    global retrieve_vendor_inventory, vendor_inventory, db_vendor

    # Data and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # List to store data and show on dashboard
    vendor_inventory = []
    vendor_rfq_list = []
    vendor_po = []
    vendor_onto_order = []
    vendor_invoice_needed = []
    vendor_pp = []
    total_income = 0
    due_payment = 0

    # Fetching the data from mongo db
    retrieve_vendor_inventory = collection_products.find({"vendor": cluster_name})
    retrieve_rfq = db_vendor[cluster_name].find({"status": "rfq"})
    retrieve_po = db_vendor[cluster_name].find({"status": "purchased"})
    retrieve_oo = db_vendor[cluster_name].find({"status": "onto_order"})
    retrieve_in = db_vendor[cluster_name].find({"status": "invoice_needed"})
    retrieve_pp = db_vendor[cluster_name].find({"status": "paid_pending"})
    retrieve_is = db_vendor[cluster_name].find({"status": "invoice_sent"})

    # Appendig the list
    for documents in retrieve_vendor_inventory:
        vendor_inventory.append(documents)

    for documents in retrieve_rfq:
        vendor_rfq_list.append(documents)

    for documents in retrieve_po:
        vendor_po.append(documents)

    for documents in retrieve_oo:
        vendor_onto_order.append(documents)

    for documents in retrieve_in:
        vendor_invoice_needed.append(documents)

    # Getting the total sale and appending the list
    for documents in retrieve_is:
        str_price = int(documents["total_price"])
        total_income += str_price
        print(total_income)

    # Getting total due
    for documents in retrieve_pp:
        str_price = int(documents["total_price"])
        due_payment += due_payment
        vendor_pp.append(documents)

    print(total_income, " Total ")

    # Retuning to home vendor
    return render_template('vendor.html', date=date, vendor_inventory=vendor_inventory, cluster_name=cluster_name,
                           vendor_rfq_list=vendor_rfq_list, vendor_po=vendor_po,
                           vendor_onto_order=vendor_onto_order, vendor_invoice_needed=vendor_invoice_needed,
                           total_income=total_income, vendor_pp=vendor_pp, due_payment=due_payment)


# Routing to vendor account
@app.route('/vendor_account')
def vendor_account():

    # accessing global variable
    global vendor

    # Accessing data and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Finding the vendor account
    vend_account_dick = account_vendor_collection.find_one({"Vendor_name": vendor})

    # Returnig vendor account
    return render_template('vendor-account.html', date=date, vendor=vendor, vend_account_dick=vend_account_dick)


# Routing to inventory
@app.route('/inventory')
def inventory():
    # time and data
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Routing to vendor inventory
    return render_template('vendor-inventory.html', date=date, vendor_inventory=vendor_inventory, vendor=vendor)


# Method to pass product data
@app.route('/pass_information', methods=['POST'])
def pass_information():
    button_value = ""
    words = []

    # Date and time
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Storing button value
    button_value = request.form['product-button']

    # Separating the button value
    words = [w.strip() for w in button_value.split()]

    # Product id
    p_id = words[0]

    # name
    name = words[1]

    # Quantity
    quantity = words[2]

    # Price
    price = words[3]

    return redirect(url_for('vendor_single_inventory', date=date, vendor=vendor,
                            p_id=p_id, name=name, quantity=quantity, price=price))


@app.route('/vendor-single-inventory/<p_id>/<name>/<quantity>/<price>')
def vendor_single_inventory(p_id, name, quantity, price):
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor-single-inventory.html', date=date, vendor=vendor,
                           p_id=p_id, name=name, quantity=quantity, price=price)


@app.route('/vendor_add_product_page')
def vendor_add_product_page():
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor-add-product.html', date=date, vendor=vendor)


@app.route('/vendor_add_product', methods=['POST'])
def vendor_add_product():
    global vendor, collection_products, vendor_inventory
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    prod_name = request.form['product_name']
    prod_id = int(request.form['product_id'])
    prod_quantity = int(request.form['quantity'])
    prod_price = request.form['price']
    prod_category = request.form.get("category")

    print(prod_name, " ", prod_id, " ", prod_quantity, " ", prod_price,
          " ", prod_category)

    post = {
        "_id": prod_id,
        "quantity": prod_quantity,
        "productId": prod_id,
        "productName": prod_name,
        "price": prod_price,
        "category": prod_category,
        "vendor": vendor,
        "added_count": 0
    }
    collection_products.insert_one(post)
    return render_template('vendor.html', date=date, vendor_inventory=vendor_inventory, cluster_name=vendor)


@app.route('/vendor_rfq')
def vendor_rfq():
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_rfq = db_vendor[vendor].find({"status": "rfq"})

    group_data = {}
    for key, group in groupby(retrieve_rfq, key=lambda x: x['product_Customer']):
        group_data[key] = list(group)

    rfq_dic = []
    for document in retrieve_rfq:
        rfq_dic.append(document)

    return render_template('vendor-rfq.html', date=date, data=group_data, vendor=vendor)


@app.route('/rfq_pass_data', methods=['POST'])
def rfq_pass_data():
    button_value = request.form['my-button']
    words = [w.strip() for w in button_value.split()]
    p_name = words[0]
    p_price = words[1]
    p_customer = words[2]
    p_id = words[3]
    s_quantity = words[4]
    print("P Name : ", p_name,
          "\nP price : ", p_price,
          "\nP customer : ", p_customer,
          "\nP ID : ", p_id,
          "\nS Quantity : ", s_quantity)
    return redirect(url_for('vendor_rfq_product', p_id=p_id, p_name=p_name, s_quantity=s_quantity,
                            p_price=p_price, p_customer=p_customer))


@app.route('/vendor_rfq_product/<p_id>/<p_name>/<s_quantity>/<p_price>/<p_customer>')
def vendor_rfq_product(p_id, p_name, s_quantity, p_price, p_customer):
    global vendor, collection_products
    message = ""

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    one_product = collection_products.find_one({"productId": int(p_id)})

    available_quantity = int(one_product['quantity'])

    if int(s_quantity) > available_quantity:
        print("No product available")
        message = "Warning : Not enough product available. Decline"
    else:
        message = "There are enough products in inventory"

    return render_template('vendor-rfq-product.html', date=date, vendor=vendor,
                           p_id=p_id, p_name=p_name, s_quantity=s_quantity
                           , p_price=p_price, p_customer=p_customer, one_product=one_product,
                           message=message)


@app.route('/vendor_sent_quote', methods=['POST'])
def vendor_sent_quote():
    global vendor, db_vendor, db_customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    contract_renewal = ""

    if "send_quote" in request.form:
        button_value = request.form['send_quote']
        words = [w.strip() for w in button_value.split()]
        p_id = int(words[0])
        cus_name = words[1]

        total_price = request.form['price']
        period = int(request.form['period'])

        if period > 0:
            contract_renewal = "deadline"
        else:
            contract_renewal = "deadline_not"

        query = {"product_Id": p_id, "product_Customer": cus_name}
        query2 = {"product_id": p_id, "product_Customer": cus_name}

        new_value = {"$set": {"total_price": total_price, "period": period, "status": "rfq_sent",
                              "contract_renewal": contract_renewal}}

        update = db_customer[cus_name].update_one(query, new_value)
        update2 = db_vendor[vendor].update_one(query2, new_value)

        print(update.modified_count, " ", update2.modified_count)

        return render_template('vendor-inventory.html', date=date, vendor_inventory=vendor_inventory, vendor=vendor)

    elif "decline_quote" in request.form:
        button_values = request.form['decline_quote']
        words = [w.strip() for w in button_values.split()]
        p_id = int(words[0])
        cus_name = words[1]
        db_vendor[vendor].delete_one({"product_id": p_id, "product_Customer": cus_name})
        db_customer[cus_name].delete_one({"product_Id": p_id, "product_Customer": cus_name})
        return render_template('vendor-inventory.html', date=date, vendor_inventory=vendor_inventory, vendor=vendor)


@app.route('/vendor_purchase_order')
def vendor_purchase_order():
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    retrieve_po = db_vendor[vendor].find({"status": "purchased"})
    print(retrieve_po, " values")
    rp = []
    for i in retrieve_po:
        print(i, " ")
        rp.append(i)

    return render_template('vendor-purchase-order.html', vendor=vendor, date=date, rp=rp)


@app.route('/send_order', methods=['POST'])
def send_order():
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = request.form['send-button']
    words = [w.strip() for w in button_value.split()]
    prd_id = int(words[0])
    cus_name = words[1]
    vend_name = words[2]
    print(prd_id, " ", cus_name, " ", vend_name)

    vendor_query = {"status": "purchased", "product_id": prd_id, "product_Customer": cus_name}
    customer_query = {"status": "purchased", "product_Id": prd_id, "product_Vendor": vend_name}

    update_values = {"$set": {"status": "onto_order"}}

    update_ven = db_vendor[vend_name].update_one(vendor_query, update_values)
    update_cus = db_customer[cus_name].update_one(customer_query, update_values)

    print("Modified Count at Vendor Collection ", update_ven.modified_count)
    print("Modified Count at Customer Collection ", update_cus.modified_count)

    return render_template('vendor.html', date=date, vendor_inventory=vendor_inventory, cluster_name=vendor)


@app.route('/vendor_order_page')
def vendor_order_page():
    global vendor, db_vendor

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # For items to be delivered
    retrieve_po = db_vendor[vendor].find({"status": "purchased"})

    to_deliver = []
    print("\nItems to be delivered")

    for document in retrieve_po:
        to_deliver.append(document)
        print(document)

    # Items which were on delivery - travelling
    retrieve_oo = db_vendor[vendor].find({"status": "onto_order"})

    onto_delivery = []
    print("\n\nItems That are travelling")

    for document in retrieve_oo:
        onto_delivery.append(document)
        print(document)

    # Items that go received but not paid
    retrieve_pp = db_vendor[vendor].find({"status": "paid_pending"})

    pending_payment = []
    print("\n\nItems got received but not get paid")

    for document in retrieve_pp:
        pending_payment.append(document)
        print(document)

    # Items that got paid and invoice needed to be send
    retrieve_is = db_vendor[vendor].find({"status": "invoice_needed"})

    invoice_to_send = []
    print("\n\nItems got paid and Invoice need to be sent")

    for document in retrieve_is:
        invoice_to_send.append(document)
        print(document)

    return render_template('vendor-order.html', date=date, vendor=vendor, to_deliver=to_deliver,
                           onto_delivery=onto_delivery, pending_payment=pending_payment,
                           invoice_to_send=invoice_to_send)


@app.route('/vendor_sent_invoice', methods=['POST'])
def vendor_sent_invoice():
    global vendor, db_vendor, db_customer

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    button_value = request.form['sent-invoice']
    words = [w.strip() for w in button_value.split()]

    prod_id = int(words[0])
    prod_customer = words[1]

    vendor_query = {"status": "invoice_needed", "product_id": prod_id, "product_Customer": prod_customer}
    customer_query = {"status": "invoice_needed", "product_Id": prod_id, "product_Vendor": vendor}

    update_values = {"$set": {"status": "invoice_sent", "contract_renewal": "not"}}

    update_vendor = db_vendor[vendor].update_one(vendor_query, update_values)
    update_customer = db_customer[prod_customer].update_one(customer_query, update_values)

    print("Modified Count at Vendor Collection ", update_vendor.modified_count)
    print("Modified Count at Customer Collection ", update_customer.modified_count)

    return render_template('vendor.html', date=date, vendor_inventory=vendor_inventory, cluster_name=vendor)


@app.route('/vendor_invoice_page')
def vendor_invoice_page():
    global vendor, db_vendor

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    retrieve_invoices = db_vendor[vendor].find({"status": "invoice_sent"})
    ri = []

    for document in retrieve_invoices:
        ri.append(document)

    return render_template('vendor-invoice.html', date=date, vendor=vendor, ri=ri)


@app.route('/create_clusters_customer', methods=['POST'])
def create_clusters_customer():
    global collection_customer, customer
    # Get the form data
    collection_customer = request.form['cluster_customer_name']
    cluster_number = request.form['cluster_number']
    cluster_email = request.form['cluster_email']
    cluster_password = request.form['cluster_password']

    customer = collection_customer

    # Create the clusters
    for i in range(1):
        collection_name = f"{collection_customer}"
        create_cluster_customer(collection_name, cluster_number, cluster_email, cluster_password)

    # Return a success message
    return redirect(url_for('signup_customer2'))


def create_cluster_customer(collection_name, cluster_number, cluster_email, cluster_password):
    global cluster, db_customer

    # Create the new cluster
    db_customer.create_collection(collection_name)

    post = {
        "Customer_name": collection_name,
        "Customer_email": cluster_email,
        "Customer_PhoneNo": cluster_number,
        "Customer_Password": cluster_password
    }
    account_customer_collection.insert_one(post)


@app.route('/insert_signup_customer2', methods=['POST'])
def insert_signup_customer2():
    global collection_customer, cluster, db_customer, account_customer_collection
    # Get the form data
    cluster_company = request.form['cluster_company']
    cluster_address = request.form['cluster_address']
    cluster_tax_no = request.form['cluster_taxNo']
    cluster_shipping = request.form['cluster_shipping']
    cluster_business = request.form['cluster_business']

    post = {
        "Customer_company": cluster_company,
        "Customer_ComAddress": cluster_address,
        "Customer_TaxNo": cluster_tax_no,
        "Customer_Shipping": cluster_shipping,
        "Customer_business": cluster_business
    }
    account_customer_collection.update_one({"Customer_name": collection_customer}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_customer3'))


@app.route('/insert_signup_customer3', methods=['POST'])
def insert_signup_customer3():
    global collection_customer, cluster, db_customer, account_customer_collection
    # Get the form data
    cluster_payment_term = request.form['cluster_paymentTerm']
    cluster_name_card = request.form['cluster_nameCard']
    cluster_card_no = request.form['cluster_cardNo']
    cluster_card_ex = request.form['cluster_cardEx']
    cluster_cvc = request.form['cluster_cvc']

    post = {
        "Customer_Payment_Term": cluster_payment_term,
        "Customer_NameCard": cluster_name_card,
        "Customer_cardNo": cluster_card_no,
        "Customer_cardEx": cluster_card_ex,
        "Customer_cvc": cluster_cvc
    }
    account_customer_collection.update_one({"Customer_name": collection_customer}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('home_customer', cluster_name=f"{collection_customer}"))


@app.route('/login_page_customer')
def login_page_customer():
    return render_template('login-customer.html')


@app.route('/login_customer', methods=['POST'])
def login_customer():
    global customer
    # Get the customer_name and password from the form
    customer_name = request.form['customer_name']
    # Check if the collection is available in the database
    if customer_name in db_customer.list_collection_names():
        customer = customer_name
        return redirect(url_for('home_customer', cluster_name=customer))
    else:
        return redirect(url_for('login_page_customer'))


@app.route('/home_customer/<cluster_name>')
def home_customer(cluster_name):
    global db_customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    storage_db = cluster["Storage"]
    product_collection = storage_db["Inventory"]
    retrieve_products = product_collection.find()

    product_list = []

    for documents in retrieve_products:
        product_list.append(documents)

    # One-hot encode the categorical variables
    categories = set(p["category"] for p in product_list)
    vendors = set(p["vendor"] for p in product_list)
    enc = OneHotEncoder(categories=[list(categories), list(vendors)])
    x_cat = [[p["category"], p["vendor"]] for p in product_list]
    x_cat_enc = enc.fit_transform(x_cat).toarray()

    # Combine the one-hot encoded categorical variables with the numerical variables
    x_num = [[p["added_count"]] for p in product_list]
    x = np.hstack([x_cat_enc, x_num])

    # Create the k-NN model
    n_neighbors = 3
    knn = NearestNeighbors(n_neighbors=n_neighbors)

    # Fit the model to the data
    knn.fit(x)

    # Choose a random product as the query
    query_index = random.randint(0, len(product_list) - 1)
    query = x[query_index]

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

    retrieve_ar = db_customer[cluster_name].find({"status": "rfq_sent"})
    request_accept = []

    for document in retrieve_ar:
        request_accept.append(document)

    retrieve_ud = db_customer[cluster_name].find({"status": "onto_order"})
    upcoming_delivery = []

    for document in retrieve_ud:
        upcoming_delivery.append(document)

    retrieve_pd = db_customer[cluster_name].find({"status": "paid_pending"})
    payment_du = []

    for document in retrieve_pd:
        payment_du.append(document)

    retrieve_cr = db_customer[cluster_name].find({"contract_renewal": "deadline"})
    contract_renewal = []

    for document in retrieve_cr:
        contract_renewal.append(document)

    retrieve_orders = db_customer[cluster_name].find({"status": "invoice_sent"})
    invoice = []

    for document in retrieve_orders:
        invoice.append(document)

    ro = db_customer[cluster_name].find({"status": "invoice_sent"})

    group_data = {}
    for key, group in groupby(ro, key=lambda x: x['category']):
        group_data[key] = list(group)

    invoice2 = []

    for document in ro:
        invoice2.append(document)

    return render_template('customer.html', date=date, suggested_products=suggested_products, cluster_name=cluster_name,
                           request_accept=request_accept, upcoming_delivery=upcoming_delivery, payment_du=payment_du,
                           contract_renewal=contract_renewal, invoice=invoice, data=group_data)


@app.route('/customer_account')
def customer_account():
    global customer, account_customer_collection
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    cus_account_dick = account_customer_collection.find_one({"Customer_name": customer})

    return render_template('customer-account.html', date=date, customer=customer, cus_account_dick=cus_account_dick)


@app.route('/products')
def products():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer-products.html', date=date, customer_products=customer_products, customer=customer)


@app.route('/pass_data', methods=['POST'])
def pass_data():
    global product_name, product_price, product_quantity, \
        product_vendor, product_customer, product_id, category, \
        account_vendor_collection

    button_value = ""
    words = []
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = request.form['my-button']
    words = [w.strip() for w in button_value.split()]
    print(words)
    product_name = words[0]
    product_price = words[1]
    product_quantity = words[2]
    product_vendor = words[3]
    product_customer = words[4]
    product_id = int(words[5])
    category = words[6]

    print("Product_Name : ", product_name,
          "\nProduct_Price : ", product_price,
          "\nProduct_Quantity : ", product_quantity,
          "\nProduct_Vendor : ", product_vendor,
          "\nProduct_Customer : ", product_customer,
          "\nProduct_Id : ", product_id,
          "Category :", category)

    return redirect(url_for('customer_single_product', date=date, customer=customer,
                            product_name=product_name, product_price=product_price, product_quantity=product_quantity,
                            product_vendor=product_vendor, product_customer=product_customer, product_id=product_id,
                            category=category))


@app.route('/customer-single-product/<product_name>/<product_price>/<product_quantity>'
           '/<product_vendor>/<product_customer>/<product_id>/<category>')
def customer_single_product(product_name, product_price, product_quantity, product_vendor, product_customer,
                            product_id, category):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    vendor_data = account_vendor_collection.find_one({"Vendor_name": product_vendor})
    return render_template('customer-single-product.html', date=date, customer=customer,
                           product_name=product_name, product_price=product_price, product_quantity=product_quantity,
                           product_vendor=product_vendor, product_customer=product_customer, product_id=product_id,
                           category=category, vendor_data=vendor_data)


@app.route("/add_cart", methods=['POST'])
def add_cart():
    global db_customer, product_name, product_price \
        , product_vendor, customer, product_id, category
    quantity = request.form["quantity"]

    post = {
        "product_Name": product_name,
        "product_Id": int(product_id),
        "product_Price": product_price,
        "product_Vendor": product_vendor,
        "selected_Quantity": quantity,
        "product_Customer": customer,
        "category": category,
        "status": "cart"
    }
    temp_collection = db_customer[customer]
    temp_collection.insert_one(post)
    return redirect(url_for('products'))


@app.route('/cart')
def cart():
    global carts, customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_carts = db_customer[customer].find({"status": "cart"})
    carts = []
    for document in retrieve_carts:
        carts.append(document)
        print(document)

    return render_template('customer-cart.html', date=date, cart=carts, customer=customer)


@app.route("/rfq", methods=['POST'])
def rfq():
    global carts, collection_products
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = ""
    words = []
    button_value = request.form['my-button']
    words = [w.strip() for w in button_value.split()]

    str_id = words[0]
    obj_id = ObjectId(str_id)
    print(type(str_id), " ", str_id)
    print(type(obj_id), " ", obj_id)
    name = words[1]
    price = words[2]
    quantity = words[3]
    vendor_name = words[4]
    customer_name = words[5]
    p_id = int(words[6])

    customer_str = "" + customer_name

    count_query = collection_products.find_one({"productName": name})
    added_count = int(count_query["added_count"]) + 1

    collection_products.update_one({"productId": p_id}, {"$set": {"added_count": added_count}})
    temp_collection_vendor = db_vendor[vendor_name]
    temp_collection_customer = db_customer[customer_name]

    post = {
        "product_Name": name,
        "product_id": p_id,
        "product_Price": price,
        "selected_quantity": quantity,
        "product_Customer": customer_name,
        "status": "rfq"
    }

    temp_collection_vendor.insert_one(post)
    update = temp_collection_customer.update_one({"_id": obj_id}, {"$set": {"status": "rfq"}})
    print(update.matched_count, " matched")
    print(update.modified_count, " modified")
    return render_template('customer-cart.html', date=date, cart=carts, customer=customer_name)


@app.route('/customer_rfq')
def customer_rfq():
    global carts, customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_rfq = db_customer[customer].find({"status": "rfq"})
    rfq_dic = []

    for document in retrieve_rfq:
        rfq_dic.append(document)

    retrieve_rfq_update = db_customer[customer].find({"status": "rfq_sent"})
    ref_upt_dick = []

    for document1 in retrieve_rfq_update:
        ref_upt_dick.append(document1)

    return render_template('customer-rfq.html', date=date, rfq_dic=rfq_dic, ref_upt_dick=ref_upt_dick,
                           customer=customer)


@app.route("/customer_rfq_proceed", methods=['POST'])
def customer_rfq_proceed():
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = ""
    words = []
    button_value = request.form['accept']
    words = [w.strip() for w in button_value.split()]
    p_name = words[0]
    p_vendor = words[1]

    retrieve_quote = db_customer[customer].find({"status": "rfq_sent", "product_Name": p_name,
                                                 "product_Vendor": p_vendor})
    rq = []

    for document in retrieve_quote:
        rq.append(document)
        print(document)
    return redirect(url_for('customer_rfq_proceed_page', p_name=p_name, p_vendor=p_vendor))


@app.route('/customer_rfq_proceed_page/<p_name>/<p_vendor>')
def customer_rfq_proceed_page(p_name, p_vendor):
    global customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_quote = db_customer[customer].find_one({"status": "rfq_sent", "product_Name": p_name,
                                                     "product_Vendor": p_vendor})

    return render_template("customer-rfq-proceed.html", date=date, customer=customer, retrieve_quote=retrieve_quote)


@app.route('/proceed_po', methods=['POST'])
def proceed_po():
    global customer, db_customer, db_vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    if "proc-po" in request.form:
        button_value = request.form['proc-po']
        words = [w.strip() for w in button_value.split()]

        p_id = int(words[0])
        p_vendor = words[1]

        return redirect(url_for('customer_proceed_page', p_id=p_id, p_vendor=p_vendor))

    elif "dic_po" in request.form:
        button_values = request.form['dic_po']
        words = [w.strip() for w in button_values.split()]

        p_id = int(words[0])
        p_vendor = words[1]

        db_vendor[p_vendor].delete_one({"product_id": p_id, "product_Customer": customer, "status": "rfq_sent"})
        db_customer[customer].delete_one({"product_Id": p_id, "product_Vendor": p_vendor, "status": "rfq_sent"})

        return render_template('customer-products.html', date=date, customer_products=customer_products,
                               customer=customer)


@app.route('/customer_proceed_page/<p_id>/<p_vendor>')
def customer_proceed_page(p_id, p_vendor):
    global customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    print(p_id, " ", p_vendor, " ", customer)
    retrieve_quote2 = db_customer[customer].find_one({"status": "rfq_sent", "product_Id": int(p_id),
                                                      "product_Vendor": p_vendor})
    print(retrieve_quote2)
    return render_template('customer-proceed.html', date=date, customer=customer, retrieve_quote2=retrieve_quote2)


@app.route('/order_purchase', methods=['POST'])
def order_purchase():
    global customer, db_customer, db_vendor, collection_products

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_values = request.form['proceed-po']
    words = [w.strip() for w in button_values.split()]
    print(words)
    prod_id = int(words[0])
    vend_name = words[1]

    delivery_date = now + timedelta(days=5)
    str_delivery_date = delivery_date.strftime("%d/%m/%Y")

    retrieve_quote2 = db_customer[customer].find_one({"status": "rfq_sent", "product_Id": prod_id,
                                                      "product_Vendor": vend_name})

    selected_quantity = int(retrieve_quote2['selected_Quantity'])

    query_customer = {"status": "rfq_sent", "product_Id": prod_id, "product_Vendor": vend_name}
    query_vendor = {"status": "rfq_sent", "product_id": prod_id, "product_Customer": customer}

    update_values = {"$set": {"status": "purchased", "delivery": "Destination", "delivery_date": str_delivery_date}}

    update_customer = db_customer[customer].update_one(query_customer, update_values)
    update_vendor = db_vendor[vend_name].update_one(query_vendor, update_values)

    quantity_query = collection_products.find_one({"productId": prod_id})
    reduce_quantity = int(quantity_query['quantity']) - selected_quantity

    collection_products.update_one({"productId": prod_id}, {"$set": {"quantity": reduce_quantity}})

    print("Modified Count at Vendor Collection ", update_vendor.modified_count)
    print("Modified Count at Customer Collection ", update_customer.modified_count)
    print("Modified Count at storage ", collection_products.modified_count)

    return render_template('customer-products.html', date=date, customer_products=customer_products, customer=customer)


@app.route('/customer_orders_page')
def customer_orders_page():
    global customer, db_customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    retrieve_so = db_customer[customer].find({"status": "onto_order"})
    print(retrieve_so, " values")
    ro = []
    for i in retrieve_so:
        print(i, " ")
        ro.append(i)

    retrieve_pp = db_customer[customer].find({"status": "paid_pending"})
    pp = []
    for document in retrieve_pp:
        pp.append(document)

    retrieve_invoice_waiting = db_customer[customer].find({"status": "invoice_needed"})
    riw = []
    for document in retrieve_invoice_waiting:
        riw.append(document)
        print(document)

    return render_template('customer-orders.html', customer=customer, date=date, ro=ro, pp=pp, riw=riw)


@app.route('/customer_order_received', methods=['POST'])
def customer_order_received():
    global customer, db_customer, db_vendor

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    button_value = request.form['order-received']
    words = [w.strip() for w in button_value.split()]

    prd_vendor = words[0]
    prd_id = int(words[1])

    query_customer = {"status": "onto_order", "product_Id": prd_id, "product_Vendor": prd_vendor}
    query_vendor = {"status": "onto_order", "product_id": prd_id, "product_Customer": customer}

    update_values = {"$set": {"status": "paid_pending"}}

    update_cus = db_customer[customer].update_one(query_customer, update_values)
    update_vend = db_vendor[prd_vendor].update_one(query_vendor, update_values)

    print("Modified Count at Vendor Collection ", update_cus.modified_count)
    print("Modified Count at Customer Collection ", update_vend.modified_count)

    return render_template('customer.html', date=date, customer_products=customer_products, cluster_name=customer)


@app.route('/pass_payment_page', methods=['POST'])
def pass_payment_page():
    button_value = request.form['proceed-pay']
    words = [w.strip() for w in button_value.split()]

    prod_vendor = words[0]
    prod_id = int(words[1])
    return redirect(url_for('customer_order_pay', prod_vendor=prod_vendor, prod_id=prod_id))


@app.route('/customer_order_pay/<prod_vendor>/<prod_id>')
def customer_order_pay(prod_vendor, prod_id):
    global customer, db_customer, account_customer_collection
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    prod_id = int(prod_id)
    print(prod_vendor, " ", prod_id, " ", customer)
    retrieve_on_product = db_customer[customer].find_one({"product_Id": prod_id, "product_Vendor": prod_vendor,
                                                          "status": "paid_pending"})
    print(retrieve_on_product, " details product")
    customer_detail = account_customer_collection.find_one({"Customer_name": customer})
    print(customer_detail, " details customer")

    return render_template('customer-order-pay.html', customer=customer, date=date,
                           retrieve_on_product=retrieve_on_product, customer_detail=customer_detail)


@app.route('/pay_order', methods=['POST'])
def pay_order():
    global customer, db_customer, db_vendor

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    button_values = request.form['pay']
    words = [w.strip() for w in button_values.split()]

    print(words, " testing values")

    prd_id = int(words[0])
    prd_vendor = words[1]

    query_customer = {"status": "paid_pending", "product_Id": prd_id, "product_Vendor": prd_vendor}
    query_vendor = {"status": "paid_pending", "product_id": prd_id, "product_Customer": customer}

    update_values = {"$set": {"status": "invoice_needed"}}

    up_cus = db_customer[customer].update_one(query_customer, update_values)
    up_ven = db_vendor[prd_vendor].update_one(query_vendor, update_values)

    print("Invoice modified Count at Vendor Collection ", up_ven.modified_count)
    print("Invoice modified Count at Customer Collection ", up_cus.modified_count)

    return render_template('customer.html', date=date, customer_products=customer_products, cluster_name=customer)


@app.route('/customer_invoice')
def customer_invoice():
    global customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_invoice = db_customer[customer].find({"status": "invoice_sent"})
    invoice = []
    for document in retrieve_invoice:
        invoice.append(document)
        print(document)

    return render_template('customer-invoice.html', date=date, customer=customer, invoice=invoice)


if __name__ == "__main__":
    app.run(debug=True)
