from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from apiflask import Schema

class FarmerInSchema(Schema):
    name = String(required=True)
    phone = String(required=True)
    location = String(required=True)

class FarmerOutSchema(Schema):
    name = String()
    phone = String()
    location = String()