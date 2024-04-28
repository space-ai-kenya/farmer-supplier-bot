<<<<<<< HEAD
from database.db import db  # Import your database setup
from database.models import Order, Farmer  # Adjust import paths as necessary


def get_order_details(order_id):
    order = db.session.query(Order, Farmer).join(Farmer, Order.farmerID == Farmer.farmerID).filter(Order.orderID == order_id).first()
    return order



=======
from database.db import db  # Import your database setup
from database.models import Order, Farmer  # Adjust import paths as necessary


def get_order_details(order_id):
    order = db.session.query(Order, Farmer).join(Farmer, Order.farmerID == Farmer.farmerID).filter(Order.orderID == order_id).first()
    return order



>>>>>>> main
