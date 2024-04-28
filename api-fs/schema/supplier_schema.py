from apiflask.fields import Integer, String, DateTime
from apiflask.validators import Length, OneOf
from apiflask import Schema, fields
from datetime import datetime, timezone
import base64



class SupplierInSchema(Schema):
    name = String(required=True)
    phone = String(required=True)
    location = String()
    county = String(required=True)
    email = String()
    password = String()