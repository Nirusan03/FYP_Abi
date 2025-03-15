# Mediquick - Medical Inventory and Procurement System

## Table of Contents
- [Mediquick - Medical Inventory and Procurement System](#mediquick---medical-inventory-and-procurement-system)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [MongoDB Cluster Information](#mongodb-cluster-information)
  - [Setting Up the Project](#setting-up-the-project)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Running the Project](#running-the-project)
    - [Start the Flask Server](#start-the-flask-server)
    - [Access the Application](#access-the-application)
  - [Machine Learning Model](#machine-learning-model)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Products](#products)
    - [RFQ (Request for Quote)](#rfq-request-for-quote)
    - [Orders](#orders)
    - [Invoices](#invoices)
  - [User Roles](#user-roles)
    - [Customer](#customer)
    - [Vendor](#vendor)
  - [Contributors](#contributors)
  - [License](#license)

---

## Project Overview
Mediquick is a **Flask-based Medical Inventory and Procurement System** that allows customers and vendors to manage medical supplies efficiently. The system enables:
- Customers to browse, request quotes, and place orders for medical products.
- Vendors to manage inventory, respond to RFQs, and process orders.
- Secure authentication using JWT-based login.
- Integration with a **Machine Learning model** for predicting optimal stock levels.

---

## Features
- **User Authentication**: Customers and vendors have separate login access.
- **Product Management**: Vendors can add, edit, and manage stock.
- **RFQ (Request for Quote)**: Customers can request pricing quotes from vendors.
- **Order Processing**: Vendors approve and ship orders.
- **Invoice Generation**: Automatic invoice generation for purchases.
- **Payment Processing**: Customers can securely complete payments.
- **Dashboard Analytics**: Summary of stock, pending orders, and financial transactions.

---

## Tech Stack
- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Database**: MongoDB Atlas (Cloud-based cluster)
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Deployment**: Docker, Gunicorn

---

## MongoDB Cluster Information
- **Database Name**: `mediquick_db`
- **Collections**:
  - `users` - Stores user credentials and roles.
  - `products` - Stores all product details.
  - `rfq` - Stores RFQs submitted by customers.
  - `orders` - Tracks orders placed and their statuses.
  - `invoices` - Stores invoice details for purchases.
- **MongoDB Atlas Connection URI:** `mongodb+srv://<username>:<password>@cluster0.mongodb.net/mediquick_db?retryWrites=true&w=majority`

---

## Setting Up the Project
### Prerequisites
- Python 3.10+
- MongoDB Atlas Account
- Node.js (if modifying frontend)

### Installation Steps
1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourrepo/mediquick.git
   cd mediquick
   ```
2. **Create a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up MongoDB Atlas**:
   - Create a cluster.
   - Update the `MONGO_URI` in `config.py`.

---

## Running the Project
### Start the Flask Server
```sh
python app.py
```
### Access the Application
- **Frontend**: `http://127.0.0.1:5000`
- **API Base URL**: `http://127.0.0.1:5000/api/`

---

## Machine Learning Model
- **Model Type**: Random Forest Regression
- **Purpose**: Predicts stock requirements based on historical order data.
- **Libraries Used**: `scikit-learn`, `pandas`, `numpy`
- **Model Training**:
  ```sh
  python train_model.py
  ```
- **Predictions Endpoint**:
  - `POST /api/predict-stock` - Takes product ID and returns recommended stock quantity.

---

## API Endpoints
### Authentication
- `POST /api/login` - Login with email and password.
- `POST /api/register` - Register a new user.

### Products
- `GET /api/products` - Retrieve all products.
- `POST /api/products/add` - Add a new product.
- `PUT /api/products/update/<id>` - Update product details.
- `DELETE /api/products/delete/<id>` - Remove a product.

### RFQ (Request for Quote)
- `POST /api/rfq/submit` - Submit an RFQ.
- `GET /api/rfq/view/<customer_id>` - View submitted RFQs.

### Orders
- `POST /api/orders/place` - Place an order.
- `GET /api/orders/status/<order_id>` - Check order status.

### Invoices
- `GET /api/invoices/<order_id>` - Retrieve invoice details.

---

## User Roles
### Customer
- Browse products.
- Request quotes.
- Place orders.
- Track order status.
- Make payments.

### Vendor
- Manage product inventory.
- Respond to RFQs.
- Process and fulfill orders.
- Generate invoices.

---

## Contributors
- **Your Name** - Developer & Maintainer
- **Your Team Members** (if any)

---

## License
This project is licensed under the MIT License.
