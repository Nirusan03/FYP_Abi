from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from bson.objectid import ObjectId
import datetime
from pymongo import *
from itertools import groupby
from datetime import date, timedelta

app = Flask(__name__)
cluster = MongoClient("mongodb://localhost:27017")

db_storage = cluster["Storage"]
collection_products = db_storage["Inventory"]

db_vendor = cluster['Vendor']
db_customer = cluster['Customer']
account_vendor_collection = db_vendor["Accounts"]
account_customer_collection = db_customer["Accounts"]

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
product_id = 0

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

    # vendor_collection = db_vendor[collection_vendor]

    post = {
        "Vendor_RegisterNo": cluster_registration_no,
        "Vendor_vat": cluster_vat,
        "Vendor_Registration": cluster_registration,
        "Vendor_regisCert": cluster_regis_cert,
        "Vendor_productCert": cluster_product_cert
    }
    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

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

    post = {
        "Vendor_bankName": cluster_bank_name,
        "Vendor_bankAddress": cluster_bank_add,
        "Vendor_AccName": cluster_acc_name,
        "Vendor_AccNo": cluster_acc_no,
        "Vendor_statement": cluster_statement
    }
    account_vendor_collection.update_one({"Vendor_name": collection_vendor}, {"$set": post}, upsert=True)

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


@app.route('/inventory')
def inventory():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor-inventory.html', date=date, upcoming_orders=product_list, vendor=vendor)


@app.route('/pass_information', methods=['POST'])
def pass_information():
    button_value = ""
    words = []
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    button_value = request.form['product-button']
    words = [w.strip() for w in button_value.split()]

    p_id = words[0]
    name = words[1]
    quantity = words[2]
    price = words[3]

    print("Product ID : ", p_id,
          "\nName : ", name,
          "\nQuantity : ", quantity,
          "\nPrice : ", price)

    return redirect(url_for('vendor_single_inventory', date=date, vendor=vendor,
                            p_id=p_id, name=name, quantity=quantity, price=price))


@app.route('/vendor-single-inventory/<p_id>/<name>/<quantity>/<price>')
def vendor_single_inventory(p_id, name, quantity, price):
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor-single-inventory.html', date=date, vendor=vendor,
                           p_id=p_id, name=name, quantity=quantity, price=price)


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
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('vendor-rfq-product.html', date=date, vendor=vendor,
                           p_id=p_id, p_name=p_name, s_quantity=s_quantity
                           , p_price=p_price, p_customer=p_customer)


@app.route('/vendor_sent_quote', methods=['POST'])
def vendor_sent_quote():
    global vendor
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    if "send_quote" in request.form:
        button_value = request.form['send_quote']
        words = [w.strip() for w in button_value.split()]
        p_id = int(words[0])
        cus_name = words[1]

        total_price = request.form['price']
        period = int(request.form['period'])

        query = {"product_Id": p_id, "product_Customer": cus_name}
        query2 = {"product_id": p_id, "product_Customer": cus_name}

        new_value = {"$set": {"total_price": total_price, "period": period, "status": "rfq_sent"}}

        update = db_customer[cus_name].update_one(query, new_value)
        update2 = db_vendor[vendor].update_one(query2, new_value)
        print(update.modified_count, " ", update2.modified_count)
        return render_template('vendor.html', date=date, upcoming_orders=product_list, cluster_name=vendor)

    elif "decline_quote" in request.form:
        return "decline quote"


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

    return render_template('vendor.html', date=date, upcoming_orders=product_list, cluster_name=vendor)


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


@app.route('/vendor_invoice_page')
def vendor_invoice_page():
    global vendor, db_vendor

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    return render_template('vendor-inventory.html', date=date, vendor=vendor)


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
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer.html', date=date, upcoming_orders=product_list, cluster_name=cluster_name)


@app.route('/products')
def products():
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer-products.html', date=date, upcoming_orders=product_list, customer=customer)


@app.route('/pass_data', methods=['POST'])
def pass_data():
    global product_name, product_price, product_quantity, \
        product_vendor, product_customer, product_id
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

    print("Product_Name : ", product_name,
          "\nProduct_Price : ", product_price,
          "\nProduct_Quantity : ", product_quantity,
          "\nProduct_Vendor : ", product_vendor,
          "\nProduct_Customer : ", product_customer,
          "\nProduct_Id : ", product_id)

    return redirect(url_for('customer_single_product', date=date, customer=customer,
                            product_name=product_name, product_price=product_price, product_quantity=product_quantity,
                            product_vendor=product_vendor, product_customer=product_customer, product_id=product_id))


@app.route('/customer-single-product/<product_name>/<product_price>/<product_quantity>'
           '/<product_vendor>/<product_customer>/<product_id>')
def customer_single_product(product_name, product_price, product_quantity, product_vendor, product_customer,
                            product_id):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    return render_template('customer-single-product.html', date=date, customer=customer,
                           product_name=product_name, product_price=product_price, product_quantity=product_quantity,
                           product_vendor=product_vendor, product_customer=product_customer, product_id=product_id)


@app.route("/add_cart", methods=['POST'])
def add_cart():
    global db_customer, product_name, product_price \
        , product_vendor, customer, product_id
    quantity = request.form["quantity"]

    post = {
        "product_Name": product_name,
        "product_Id": int(product_id),
        "product_Price": product_price,
        "product_Vendor": product_vendor,
        "selected_Quantity": quantity,
        "product_Customer": customer,
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
    global carts
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
    global customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    if "proc-po" in request.form:
        button_value = request.form['proc-po']
        words = [w.strip() for w in button_value.split()]
        p_id = int(words[0])
        p_vendor = words[1]
        return redirect(url_for('customer_proceed_page', p_id=p_id, p_vendor=p_vendor))
    elif "dic_po" in request.form:
        return "decline order"


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
    global customer
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

    query_customer = {"status": "rfq_sent", "product_Id": prod_id, "product_Vendor": vend_name}
    query_vendor = {"status": "rfq_sent", "product_id": prod_id, "product_Customer": customer}

    update_values = {"$set": {"status": "purchased", "delivery": "Destination", "delivery_date": str_delivery_date}}

    update_customer = db_customer[customer].update_one(query_customer, update_values)
    update_vendor = db_vendor[vend_name].update_one(query_vendor, update_values)

    print("Modified Count at Vendor Collection ", update_vendor.modified_count)
    print("Modified Count at Customer Collection ", update_customer.modified_count)
    return render_template('customer.html', date=date, upcoming_orders=product_list, cluster_name=customer)


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

    return render_template('customer.html', date=date, upcoming_orders=product_list, cluster_name=customer)


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

    return render_template('customer.html', date=date, upcoming_orders=product_list, cluster_name=customer)


@app.route('/customer_invoice')
def customer_invoice():
    global customer
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    retrieve_invoice = db_customer[customer].find({"status": "proceed_po"})
    invoice = []
    for document in retrieve_invoice:
        invoice.append(document)
        print(document)

    return render_template('customer-invoice.html', date=date, customer=customer, invoice=invoice)


if __name__ == "__main__":
    app.run(debug=True)
