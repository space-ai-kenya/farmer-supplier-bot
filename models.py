from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Farmer(db.Model):
    __tablename__ = 'farmers'
    farmerID =db.Column(db.Integer, primary_key = True)
    name =db.Column(db.String(500), nullable=False)
    phone =db.Column(db.String(100), nullable=False)
    location =db.Column(db.String(500), nullable=True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, name, phone, location, reg_date):
        self.name = name
        self.phone = phone
        self.location = location
        self.reg_date = reg_date


class Agent(db.Model):
    __tablename__ = 'agents'
    agentID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(100), nullable= False)
    location = db.Column(db.String(500), nullable = True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, name, phone, location, reg_date):
        self.name = name
        self.phone = phone
        self.location = location
        self.reg_date = reg_date


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplierID = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(500), nullable = False)
    phone = db.Column(db.String(100), nullable= False)
    location = db.Column(db.String(500), nullable = True)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, name, phone, location, reg_date):
        self.name = name
        self.phone = phone
        self.location = location
        self.reg_date = reg_date