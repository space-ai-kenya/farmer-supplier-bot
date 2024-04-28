<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from database.db import db
import uuid


#generate an even more unique order uuid that always starts with FO (i.e 'F'armer'O'rder)
def generate_order_uuid():
    unique_id = str(uuid.uuid4().hex)[:9]  # Take the first 14 characters of the UUID hex string
    return f"FO-{unique_id}"



class Farmer(db.Model):
    __tablename__ = 'farmers'
    farmerID =db.Column(db.Integer, primary_key = True)
    f_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())) #add County, Village, fname, middlename, lname
    name =db.Column(db.String(500), nullable=False)
    phone =db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(200), nullable=True)
    village = db.Column(db.String(255), nullable=True)
    location =db.Column(db.String(500), nullable=True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    


########## Add a 'last_updated' column to the Agent and Supplier models:
######   This can help you track when each record was last updated or modified.Example: last_updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

class Agent(db.Model):
    __tablename__ = 'agents'
    agentID = db.Column(db.Integer, primary_key = True) # Add a_uuid, county, and EMAIL for agents 
    a_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(100), nullable= False)
    county = county = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(500), nullable = True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))




class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplierID = db.Column(db.Integer, primary_key = True) # Add s_uuid, County for suppliers,
    s_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(100), nullable= False)
    county = county = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(500), nullable = True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    #last_updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))



class Order(db.Model):
    __tablename__ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    o_uuid = db.Column(db.String(36), unique=True, nullable=False, default=generate_order_uuid)
    farmerID = db.Column(db.Integer, nullable=False)
    order_desc = db.Column(db.String(65000), nullable=False)
    status = db.Column(db.String(255), default='submitted')
    orderDate = db.Column(db.DateTime, default=datetime.now(timezone.utc))
=======
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from database.db import db
import uuid
import bcrypt

#generate an even more unique order uuid that always starts with FO (i.e 'F'armer'O'rder)
def generate_order_uuid():
    unique_id = str(uuid.uuid4().hex)[:9]  # Take the first 14 characters of the UUID hex string
    return unique_id



class Farmer(db.Model):
    __tablename__ = 'farmers'
    farmerID =db.Column(db.Integer, primary_key = True)
    f_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())) #add County, Village, fname, middlename, lname
    name =db.Column(db.String(500), nullable=False)
    phone =db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(200), nullable=True)
    village = db.Column(db.String(255), nullable=True)
    location =db.Column(db.String(500), nullable=True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    orders = db.relationship('Order', back_populates='farmer')
    


########## Add a 'last_updated' column to the Agent and Supplier models:
######   This can help you track when each record was last updated or modified.Example: last_updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

class Agent(db.Model):
    __tablename__ = 'agents'
    agentID = db.Column(db.Integer, primary_key = True) # Add a_uuid, county, and EMAIL for agents 
    a_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(100), nullable= False)
    county = county = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(500), nullable = True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))




class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplierID = db.Column(db.Integer, primary_key = True) # Add s_uuid, County for suppliers,
    s_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(100), nullable= False)
    county = county = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(500), nullable = True)
    email = db.Column(db.String(255), nullable = True)
    password = db.Column(db.String(255),nullable= True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    #last_updated = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))
    
    def __init__(self, **kwargs):
        super(Supplier, self).__init__(**kwargs)
        if 'password' in kwargs:
             self.password = bcrypt.hashpw(kwargs['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        print("Encoded Password:", password.encode('utf-8'))
        print("Stored Hash:", self.password.encode('utf-8'))
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))



class Order(db.Model):
    __tablename__ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    o_uuid = db.Column(db.String(36), unique=True, nullable=False, default=generate_order_uuid)
    supplierID = db.Column(db.Integer, db.ForeignKey('suppliers.supplierID'), nullable=True)
    farmerID = db.Column(db.Integer,db.ForeignKey('farmers.farmerID'), nullable=False)
    order_desc = db.Column(db.Text, nullable=False)
    pdf_path = db.Column(db.String(255), nullable=True)  # Path to the PDF file
    status = db.Column(db.String(255), default='submitted')
    orderDate = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    farmer = db.relationship('Farmer', back_populates='orders')
>>>>>>> main
