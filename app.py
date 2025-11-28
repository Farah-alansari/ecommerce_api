from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column,relationship
from sqlalchemy import String,ForeignKey,Column,Float,Table,DateTime, select
from datetime import datetime
from marshmallow import ValidationError
#-----------------------------------------------------------------
# Create Flask app
#-----------------------------------------------------------------
app=Flask(__name__)


#-----------------------------------------------------------------
# Connect to MySQL database
#-----------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Farah%401985@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#-----------------------------------------------------------------
# Base Class
#-----------------------------------------------------------------
class Base(DeclarativeBase):
    pass

#-----------------------------------------------------------------
# Initialize database
#-----------------------------------------------------------------
db= SQLAlchemy(model_class=Base)
db.init_app(app)


#-----------------------------------------------------------------
# Initialize marshmallow
#-----------------------------------------------------------------
ma=Marshmallow(app)


#-----------------------------------------------------------------
# Association Table
#-----------------------------------------------------------------  
order_product = Table(
    'order_product',
    Base.metadata,
    Column('order_id',ForeignKey("orders.id"),primary_key=True),
    Column('product_id',ForeignKey("products.id"),primary_key=True)
)

#-----------------------------------------------------------------
# Users Table
#-----------------------------------------------------------------
class User(Base):
    __tablename__='users'
    id:Mapped[int]= mapped_column(primary_key= True)
    name:Mapped[str]=mapped_column(String(30))
    address:Mapped[str]=mapped_column(String(200))
    email:Mapped[str]=mapped_column(String(200),unique=True)

    orders: Mapped[list['Order']] = relationship(back_populates='user')
    

#-----------------------------------------------------------------
# Orders Table
#-----------------------------------------------------------------
class Order(Base):
    __tablename__='orders'
    id:Mapped[int]=mapped_column(primary_key=True)
    order_date:Mapped[datetime] = mapped_column(DateTime)
    user_id:Mapped[int]= mapped_column(ForeignKey('users.id'))
    
    user:Mapped['User']=relationship(back_populates='orders')
    products:Mapped[list['Product']] = relationship(secondary='order_product',back_populates='orders')
    
    
#-----------------------------------------------------------------
# Products Table
#-----------------------------------------------------------------
class Product(Base):
    __tablename__='products'
    id:Mapped[int]=mapped_column(primary_key=True)
    product_name:Mapped[str] = mapped_column(String(200))
    price:Mapped[float]=mapped_column()

    orders:Mapped[list['Order']] = relationship(secondary='order_product',back_populates='products')
    

#-----------------------------------------------------------------
# User Schema
#-----------------------------------------------------------------
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        include_relationships = True

#-----------------------------------------------------------------
# Order Schema
#-----------------------------------------------------------------
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Order
        load_instance= True
        include_fk= True
        include_relationships = True
        fields=("id","order_date","user_id","products")

    

#-----------------------------------------------------------------
# Product Schema
#-----------------------------------------------------------------
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Product
        load_instance= True
        include_fk= True
        include_relationships = True
      

     
#-----------------------------------------------------------------
# Schema Instance
#-----------------------------------------------------------------
user_schema = UserSchema()
users_schema = UserSchema(many= True)

order_schema = OrderSchema()
orders_schema= OrderSchema(many = True)

product_schema = ProductSchema()
products_schema = ProductSchema(many = True)


#-----------------------------------------------------------------
# User Endpoints 
#-----------------------------------------------------------------

# Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    query= select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200


#Retrieve a user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user= db.session.get(User,id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return user_schema.jsonify(user), 200 

#Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = request.json
        user_schema.load(user_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_user = User (
        name = user_data['name'],
        address= user_data['address'],
        email = user_data['email']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201
    
#Update a user by ID    
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User,id)
    if not user:
         return jsonify({"message": "Invalid user id"}), 400
    try:
        user_data = request.json
        user_schema.load(user_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    user.name = user_data['name']
    user.address = user_data['address']
    user.email = user_data['email']
    
    db.session.commit()
    return user_schema.jsonify(user), 200

#Delete a user by ID
@app.route('/users/<int:id>' , methods=['DELETE'])
def delete_user(id):
    user= db.session.get(User,id)
    if not user:
        return jsonify({"message":"Invalid user id"}) , 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted successfully"}), 200
    
    
    
#-----------------------------------------------------------------
# Product Endpoints 
#-----------------------------------------------------------------

# Retrieve all products
@app.route('/products', methods=['GET'])
def get_products():
    query= select(Product)
    products = db.session.execute(query).scalars().all()
    return products_schema.jsonify(products), 200


# Retrieve a product by ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product= db.session.get(Product,id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return product_schema.jsonify(product), 200 

# Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = request.json
        product_schema.load(product_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_product = Product (
        product_name = product_data['product_name'],
        price= product_data['price']
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product), 201
    
# Update a product by ID   
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product,id)
    if not product:
         return jsonify({"message": "Invalid product id"}), 400
    try:
        product_data = request.json
        product_schema.load(product_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    product.product_name = product_data['product_name']
    product.price = product_data['price']
    
    db.session.commit()
    return product_schema.jsonify(product), 200

# Delete a product by ID
@app.route('/products/<int:id>' , methods=['DELETE'])
def delete_product(id):
    product= db.session.get(Product,id)
    if not product:
        return jsonify({"message":"Invalid product id"}) , 400
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product {id} deleted successfully"}), 200
    
    

#-----------------------------------------------------------------
# Order Endpoints
#-----------------------------------------------------------------

# Create a new order (requires user ID and order date)

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = request.json
        order_schema.load(order_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_order = Order(
        user_id = order_data['user_id'],
        order_date = order_data['order_date']
    )

    db.session.add(new_order)
    db.session.commit()
    
    return order_schema.jsonify(new_order), 200

# Add a product to an order (prevent duplicates)

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id,product_id):
    order= db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    
    if not order:
        return jsonify({"message":"Order not found"}) , 400

    if not product:
        return jsonify({"message":"Product not found"}) , 400
    
    if product in order.products:
        return jsonify({"message":"Prodduct already added"}) , 400
    
    order.products.append(product)
    db.session.commit()
    
    return jsonify({"message": "Product added succesfully"}), 200


# Remove a product from an order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['Delete'])
def remove_product_from_order(order_id,product_id):
    order= db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    
    if not order:
        return jsonify({"message":"Order not found"}) , 400

    if not product:
        return jsonify({"message":"Product not found"}) , 400
    
    if product in order.products:
        return jsonify({"message":"Product not in this order"}) , 400
    
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"message": "Product removed succesfully"}), 200


# Get all orders for a user

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_for_user(user_id):
    user= db.session.get(User, user_id)
    if not user:
        return jsonify({"message":"User not found"}) , 400
    return orders_schema.jsonify(user.orders), 200
    
#  Get all products for an order

@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_products_in_order(order_id):
    order= db.session.get(Order, order_id)
    if not order:
        return jsonify({"message":"Order not found"}) , 400
    return orders_schema.jsonify(order.products), 200


#-----------------------------------------------------------------
# Home Route
#-----------------------------------------------------------------

@app.route('/')
def home():
    return "API is working."
with app.app_context():
    db.create_all()
#-----------------------------------------------------------------
# Run Server
#-----------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True) 
