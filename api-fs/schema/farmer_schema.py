from apiflask.fields import Integer, String, DateTime
from apiflask.validators import Length, OneOf
from apiflask import Schema
from datetime import datetime, timezone

class FarmerInSchema(Schema):
    name = String(required=True)
    phone = String(required=True)
    location = String(required=True)
    #reg_date = DateTime(default=datetime.now(timezone.utc), required=False)

class FarmerOutSchema(Schema):
    #farmerID = Integer()
    name = String()
    #phone = String()
    #location = String()
    #reg_date = DateTime()
    

class OrderIn(Schema):
    phone = String(required=True)
    order_desc = String(required=True)
