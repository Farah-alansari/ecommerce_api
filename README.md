# E-commerce API

A simple RESTful API using **Flask**, **SQLAlchemy**, and **Marshmallow** to manage Users, Products, and Orders.

## Features

- CRUD for Users
- CRUD for Products
- Create Orders (user_id + order_date)
- Add / Remove products in an order
- Get orders for a user
- Get products in an order
- Validation with Marshmallow
- Tested using Postman collection

## Project Structure

project/
│── app.py  
│── postman_collection.json  
│── README.md

## Technologies

- Python
- Flask
- MySQL
- SQLAlchemy
- Marshmallow
- Postman

## Run the Project

pip install -r requirements.txt  
python app.py  
Server runs at: http://127.0.0.1:5000

## API Endpoints

### Users

GET /users  
GET /users/<id>  
POST /users  
PUT /users/<id>  
DELETE /users/<id>

### Products

GET /products  
GET /products/<id>  
POST /products  
PUT /products/<id>  
DELETE /products/<id>

### Orders

POST /orders  
PUT /orders/<order_id>/add_product/<product_id>  
DELETE /orders/<order_id>/remove_product/<product_id>  
GET /orders/user/<user_id>  
GET /orders/<order_id>/products

## Postman

Import the provided file:
postman_collection.json

## ✔️ Status

Project completed and tested successfully.

### Author:

Farah Alansari
