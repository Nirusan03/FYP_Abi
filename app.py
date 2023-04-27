from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from bson.objectid import ObjectId
import datetime
from pymongo import *

app = Flask(__name__)
cluster = MongoClient("mongodb://localhost:27017")

db_storage = cluster["Storage"]
collection_products = db_storage["Inventory"]

db_vendor = cluster['Vendor']
db_customer = cluster['Customer']

customer = ""
vendor = ""

retrieve_products = collection_products.find()
product_list = []

carts = []

collection_vendor = ""
collection_customer = ""

product_name = ""
product_price = ""
product_quantity = ""
product_vendor = ""
product_customer = ""

for documents in retrieve_products:
    product_list.append(documents)


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
    return render_template('signup-customer.html')


@app.route('/signup_customer2')
def signup_customer2():
    return render_template('signup-customer2.html')


@app.route('/signup_customer3')
def signup_customer3():
    return render_template('signup-customer3.html')


@app.route('/create_clusters_vendor', methods=['POST'])
def create_clusters_vendor():
    global collection_vendor, vendor
    # Get the form data
    collection_vendor = request.form['cluster_vendor_name']
    cluster_code = request.form['cluster_code']
    cluster_phone_no = request.form['cluster_phoneNo']
    cluster_address = request.form['cluster_address']
    cluster_email = request.form['cluster_email']
    cluster_password = request.form['cluster_password']

    vendor = collection_vendor
    # Create the clusters
    for i in range(1):
        collection_name = f"{collection_vendor}"
        create_cluster_vendor(collection_name, cluster_code, cluster_phone_no,
                              cluster_address, cluster_email, cluster_password)

    # Return a success message
    # return redirect(url_for('customer', cluster_name=f"{cluster_customer}"))
    return redirect(url_for('signup_vendor2'))


def create_cluster_vendor(collection_name, cluster_code, cluster_phone_no, cluster_address, cluster_email,
                          cluster_password):
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
    temp_collection.insert_one(post)


@app.route('/insert_signup_vendor2', methods=['POST'])
def insert_signup_vendor2():
    global collection_vendor, cluster, db_vendor
    # Get the form data
    cluster_registration_no = request.form['cluster_registrationNo']
    cluster_vat = request.form['cluster_vat']
    cluster_registration = request.form['cluster_registration']
    cluster_regis_cert = request.form['cluster_regisCert']
    cluster_product_cert = request.form['cluster_productCert']

    vendor_collection = db_vendor[collection_vendor]

    post = {
        "Vendor_RegisterNo": cluster_registration_no,
        "Vendor_vat": cluster_vat,
        "Vendor_Registration": cluster_registration,
        "Vendor_regisCert": cluster_regis_cert,
        "Vendor_productCert": cluster_product_cert
    }
    vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_vendor3'))


@app.route('/insert_signup_vendor3', methods=['POST'])
def insert_signup_vendor3():
    global collection_customer, cluster, db_vendor
    # Get the form data
    cluster_bank_name = request.form['cluster_bankName']
    cluster_bank_add = request.form['cluster_bankAdd']
    cluster_acc_name = request.form['cluster_accName']
    cluster_acc_no = request.form['cluster_accNo']
    cluster_statement = request.form['cluster_statement']

    vendor_collection = db_vendor[collection_vendor]

    post = {
        "Vendor_bankName": cluster_bank_name,
        "Vendor_bankAddress": cluster_bank_add,
        "Vendor_AccName": cluster_acc_name,
        "Vendor_AccNo": cluster_acc_no,
        "Vendor_statement": cluster_statement
    }
    vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('home_vendor', cluster_name=f"{collection_vendor}"))


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


@app.route('/home_vendor/<cluster_name>')
def home_vendor(cluster_name):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor.html', date=date, upcoming_orders=product_list, cluster_name=cluster_name)


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
    temp_collection = db_customer[collection_name]

    post = {
        "Customer_name": collection_name,
        "Customer_email": cluster_email,
        "Customer_PhoneNo": cluster_number,
        "Customer_Password": cluster_password
    }
    temp_collection.insert_one(post)


@app.route('/insert_signup_customer2', methods=['POST'])
def insert_signup_customer2():
    global collection_customer, cluster, db_customer
    # Get the form data
    cluster_company = request.form['cluster_company']
    cluster_address = request.form['cluster_address']
    cluster_tax_no = request.form['cluster_taxNo']
    cluster_shipping = request.form['cluster_shipping']
    cluster_business = request.form['cluster_business']

    temp_collection = db_customer[collection_customer]

    post = {
        "Customer_company": cluster_company,
        "Customer_ComAddress": cluster_address,
        "Customer_TaxNo": cluster_tax_no,
        "Customer_Shipping": cluster_shipping,
        "Customer_business": cluster_business
    }
    temp_collection.update_one({"Customer_name": collection_customer}, {"$set": post}, upsert=True)

    # Return a success message
    return redirect(url_for('signup_customer3'))


@app.route('/insert_signup_customer3', methods=['POST'])
def insert_signup_customer3():
    global collection_customer, cluster, db_customer
    # Get the form data
    cluster_payment_term = request.form['cluster_paymentTerm']
    cluster_name_card = request.form['cluster_nameCard']
    cluster_card_no = request.form['cluster_cardNo']
    cluster_card_ex = request.form['cluster_cardEx']
    cluster_cvc = request.form['cluster_cvc']

    temp_collection = db_customer[collection_customer]

    post = {
        "Customer_Payment_Term": cluster_payment_term,
        "Customer_NameCard": cluster_name_card,
        "Customer_cardNo": cluster_card_no,
        "Customer_cardEx": cluster_card_ex,
        "Customer_cvc": cluster_cvc
    }
    temp_collection.update_one({"Customer_name": collection_customer}, {"$set": post}, upsert=True)

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
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer.html', date=date, upcoming_orders=product_list, cluster_name=cluster_name)


@app.route('/products')
def products():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer-products.html', date=date, upcoming_orders=product_list, customer=customer)


@app.route('/inventory')
def inventory():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor-inventory.html', date=date, upcoming_orders=product_list, vendor=vendor)


@app.route('/pass_data', methods=['POST'])
def pass_data():
    global product_name, product_price, product_quantity, \
        product_vendor, product_customer
    button_value = ""
    words = []
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = request.form['my-button']
    words = [w.strip() for w in button_value.split()]
    product_name = words[0]
    product_price = words[1]
    product_quantity = words[2]
    product_vendor = "Vendor" + words[3]
    product_customer = words[4]

    print("Product_Name : ", product_name,
          "\nProduct_Price : ", product_price,
          "\nProduct_Quantity : ", product_quantity,
          "\nProduct_Vendor : ", product_vendor,
          "\nProduct_Customer : ", product_customer)

    # temp_collection = db_vendor[product_vendor]
    # temp_collection.insert_one({'data': button_value})

    # return jsonify({'result': 'success'})
    return redirect(url_for('customer_single_product', date=date, customer=customer,
                            product_name=product_name, product_price=product_price, product_quantity=product_quantity,
                            product_vendor=product_vendor, product_customer=product_customer))


@app.route('/customer-single-product/<product_name>/<product_price>/<product_quantity>'
           '/<product_vendor>/<product_customer>')
def customer_single_product(product_name, product_price, product_quantity, product_vendor, product_customer):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer-single-product.html', date=date, customer=customer,
                           product_name=product_name, product_price=product_price, product_quantity=product_quantity,
                           product_vendor=product_vendor, product_customer=product_customer)


@app.route("/add_cart", methods=['POST'])
def add_cart():
    global db_customer, product_name, product_price \
        , product_vendor, customer
    quantity = request.form["quantity"]
    print("INSIDE ADD TO CART"
          "\nProduct Name : ", product_name,
          "\nProduct Price : ", product_price,
          "\nProduct Vendor : ", product_vendor,
          "\nSelected Quantity : ", quantity,
          "\nProduct Customer : ", customer)

    post = {
        "product_Name": product_name,
        "product_Price": product_price,
        "product_Vendor": product_vendor,
        "selected_Quantity": quantity,
        "product_Customer": customer,
        "status": "cart"
    }
    temp_collection = db_customer[customer]
    temp_collection.insert_one(post)
    return redirect(url_for('products'))


@app.route('/rfq_vendor')
def rfq_vendor():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('rfq-vendor.html', date=date, upcoming_orders=product_list)


@app.route('/cart')
def cart():
    global carts, customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_carts = db_customer[customer].find({"status": "cart"})
    carts = []
    for document in retrieve_carts:
        # keys = list(document.keys())
        #
        # vendor_key = keys[3]
        # vendor_value = document[vendor_key]
        #
        # vendor_collection = db_vendor[vendor_value]
        # vendor_collection.insert_one(document)

        carts.append(document)
        print(document)

    return render_template('customer-cart.html', date=date, cart=carts, customer=customer)


@app.route("/rfq", methods=['POST'])
def rfq():
    global carts
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = ""
    words = []
    button_value = request.form['my-button']
    words = [w.strip() for w in button_value.split()]

    str_id = words[0]
    obj_id = ObjectId(str_id)
    print(type(str_id), " ",  str_id)
    print(type(obj_id), " ",  obj_id)
    name = words[1]
    price = words[2]
    quantity = words[3]
    vendor = words[4]
    customer = words[5]
    customer_str = "" + customer

    temp_collection_vendor = db_vendor[vendor]
    temp_collection_customer = db_customer[customer]

    post = {
        "product_Name": name,
        "product_Price": price,
        "selected_quantity": quantity,
        "product_Customer": customer,
        "status": "rfq"
    }

    temp_collection_vendor.insert_one(post)
    update = temp_collection_customer.update_one({"_id": obj_id}, {"$set": {"status": "rfq"}})
    print(update.matched_count, " matched")
    print(update.modified_count, " modified")
    return render_template('customer-cart.html', date=date, cart=carts, customer=customer)


@app.route('/customer_rfq')
def customer_rfq():
    global carts, customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_rfq = db_customer[customer].find({"status": "rfq"})
    rfq_dic = []

    for document in retrieve_rfq:
        rfq_dic.append(document)
    return render_template('customer-rfq.html', date=date, rfq_dic=rfq_dic, customer=customer)


if __name__ == "__main__":
    app.run(debug=True)
