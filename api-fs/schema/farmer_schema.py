from apiflask.fields import Integer, String, DateTime
from apiflask.validators import Length, OneOf
from apiflask import Schema, fields
from datetime import datetime, timezone
import base64

class FarmerInSchema(Schema):
    name = String(required=True)
    phone = String(required=True)
    location = String()
    county = String(required=True)
    village = String()
    #reg_date = DateTime(default=datetime.now(timezone.utc), required=False)

class FarmerOutSchema(Schema):
    name = String()
    found= String()
    notfound = String()


class OrderformattingIn(Schema):
    order_desc = String(required=True)

class OrderformattingOut(Schema):
    formatted_order = String()

class OrderIn(Schema):
    phone = String(required=True)
    order_desc = String(required=True)
    # invoice = fields.Method('get_order')

    # def get_order(self, obj):
    # # Assuming you have the PDF file path stored in the 'invoice_filepath' attribute
    #     with open(obj.invoice_filepath, 'rb') as file:
    #         pdf_data = base64.b64encode(file.read()).decode('utf-8')
    #     return pdf_data


class CountylistOut(Schema):
    name=String()

    

   