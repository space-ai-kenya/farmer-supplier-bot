from apiflask import APIFlask, Schema, HTTPError
from flask_cors import CORS
from flask import request, jsonify, render_template, url_for, session, redirect, send_file
import os
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from sqlalchemy import func
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask_migrate import Migrate
import uuid

from twilio.rest import Client

# Local imports ------------------------------------------------
from database.models import Farmer, Order, Supplier
from schema.farmer_schema import FarmerInSchema, FarmerOutSchema, OrderIn, CountylistOut, OrderformattingIn, OrderformattingOut, MessageRequest
from database.db import db
from routes.routes import get_order_details
from routes.invoices import generate_invoice
from routes.invoices import nicely_formatted_order_gemini
from database.models import generate_order_uuid
from common.farmcardtemplate import FC_TEMPLATE

from schema.supplier_schema import SupplierInSchema

# End of local import ---------------------------------------------



load_dotenv()

#set base directory of app.py
basedir = os.path.abspath(os.path.dirname(__file__))

base_url = os.getenv('BASE_URL')
db_host = os.getenv('DB_HOST')



account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)


assistant_api_key = os.getenv('ASSISTANT_API_KEY')
assistant_url = os.getenv('ASSISTANT_URL')
assistant_id = os.getenv('ASSISTANT_ID')

authenticator = IAMAuthenticator(assistant_api_key)
assistant = AssistantV2(
    version='2023-04-15',
    authenticator=authenticator
)
assistant.set_service_url(assistant_url)



# https://stackoverflow.com/questions/68997414/sqlalchemy-exc-operationalerror-mysqldb-exceptions-operationalerror-1045


# MySQL SQLALchemy configuration 

app = APIFlask(__name__, title='', version='', static_folder='static',template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = db_host
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app, resources={r"*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

migrate = Migrate(app, db)


# Endpoint to send a message
@app.post('/whatsapp_send_message')
@app.input(MessageRequest)
def whatsapp_send_message(json_data):

    message_body = json_data['body']
    message_body = message_body.format(json_data['confirm'], json_data['cancel'])

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=message_body,
    to='whatsapp:+254799008462'
    )

    return {'message_id': message.sid}







##Endpoint for creating and inserting a farmer into db from a FORM using POST
@app.route('/', methods=['POST','GET'])
def register_farmer_form():
    if request.method == 'GET':
        # Serve HTML form
        return render_template('reg_farmer.html')
    
    elif request.method == 'POST':
        # Manually extract form data
        f_name = request.form.get('name')
        f_phone = request.form.get('phone')
        f_location = request.form.get('location')
        
        # Check if farmer already exists
        existing_farmer = Farmer.query.filter_by(phone=f_phone).first()
        if existing_farmer:
            return "Farmer is already registered."
        
        # Proceed to create and save the new farmer
        new_farmer = Farmer(name=f_name, phone=f_phone, location=f_location, reg_date=datetime.now(timezone.utc))
        try:
            db.session.add(new_farmer)
            db.session.commit()
            # Redirect or inform of successful registration
            return redirect('/')  # Adjust as needed
        except Exception as e:
            # Handle errors during save
            return f'An error occurred: {str(e)}'


##Register a farmer
@app.post('/reg_farmer')
@app.input(FarmerInSchema, location='json') 
def register_farmer(json_data):

    # Generate Farmer UUID "f_uuid" once 
    f_uuid = str(uuid.uuid4())
    farmingtype="Dairy Farmer"
    farm_name="Bomet Farm 1"

    # MySQL part 
    reg_farmer = Farmer(f_uuid=f_uuid, name=json_data['name'], phone=json_data['phone'], county=json_data['county'], village=json_data['village'], location=json_data['location'])
    db.session.add(reg_farmer)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  
        return jsonify({"message": "Could not add farmer to MySQL database. Error: {}".format(str(e)), "status": "error"}), 400
    
    FC_TEMPLATE["f_uuid"]= f_uuid
    FC_TEMPLATE["p_number"]= json_data.get("phone")
    FC_TEMPLATE["farming_type"]= farmingtype
    FC_TEMPLATE["farm_name_id"]= farm_name


    # URL 
    farmcard_api_url = f'{base_url}/farm_card/create_farmcard'

    # Try register the farmer in the external API
    try:
        response = requests.post(farmcard_api_url, json=FC_TEMPLATE, verify=False).json()
        output=dict(response)
        #response.raise_for_status()  # Raises an error for bad responses
        if output["code"]==201:
            print(output)
            return jsonify({"message": "Farmer added successfully to both MySQL and FarmCard", "status": "success", "f_uuid": f_uuid}), 200
        
    except requests.RequestException as e:
        # delete farmer in case it doesnt work
        db.session.delete(reg_farmer)
        db.session.commit()
        return jsonify({"message": "Failed to register farmer in external API. MySQL entry rolled back. Error: {}".format(str(e)), "status": "error"}), 400

    



## Get & Verify farmer registration and info using phone number
@app.get('/farmers/<string:phone_num>')
@app.output(FarmerOutSchema)  
def verify_farmer_registration(phone_num):
    farmer = Farmer.query.filter_by(phone=phone_num).first()
    if not farmer:
        # Instead of returning an HTTP error, return a schema-compliant response with a message
        return {"notfound": "Farmer not found in the system. Please make sure you are registered."}
    
    # If farmer is found, optionally add a message, or just return the farmer's details
    farmer_details = {"name": farmer.name, "found": "We have found an existing account, You are already registered."}
    return farmer_details




## Enpoint to create an store an order in db and generate an invoice----------
# @app.post('/submit_order')
# @app.input(OrderIn, location='json')
# def submit_order(json_data):

#     o_uuid = generate_order_uuid()

#     phone_num = json_data['phone']
#     farmer = Farmer.query.filter_by(phone=phone_num).first()
    
#     if not farmer:
#         raise HTTPError(404, message='Farmer not found in the system. Please make sure you are registered.')
    
#     create_order = Order(o_uuid=o_uuid, farmerID=farmer.farmerID, order_desc =json_data['order_desc'])
#     db.session.add(create_order)
#     db.session.commit()

#     ### Ensures the 'invoices' directory exists
#     if not os.path.exists('Orders'):
#         os.makedirs('Orders')

#     ### for generating invoice below
#     order_details = get_order_details(create_order.orderID)
#     invoice_filename = os.path.join('Orders', f"order_{create_order.o_uuid}.pdf")
#     generate_invoice(order_details, filename=invoice_filename)

#     pdf_file = send_file(invoice_filename, as_attachment=True), 200
#     # Return the PDF file in the response
#     return pdf_file


@app.post('/submit_order')
@app.input(OrderIn, location='json')
def submit_order(json_data):
    o_uuid = generate_order_uuid()

    phone_num = json_data['phone']
    farmer = Farmer.query.filter_by(phone=phone_num).first()
    
    if not farmer:
        raise HTTPError(404, message='Farmer not found in the system. Please make sure you are registered.')
    
    # Fetch a supplier that matches the farmer's county
    supplier = Supplier.query.filter(func.lower(Supplier.county) == func.lower(farmer.county)).first()

    if not supplier:
        raise HTTPError(404, message='No supplier available in your location.')

    create_order = Order(
        o_uuid=o_uuid,
        farmerID=farmer.farmerID,
        supplierID=supplier.supplierID,
        order_desc=json_data['order_desc']
    )
    db.session.add(create_order)
    db.session.commit()

    # Ensures the 'Orders' directory exists
    if not os.path.exists('Orders'):
        os.makedirs('Orders')

    # For generating invoice
    order_details = get_order_details(create_order.orderID)
    invoice_filename = os.path.join('Orders', f"order_FO{create_order.orderID}.pdf")
    generate_invoice(order_details, filename=invoice_filename)
    
    # Store the path to the PDF in the database
    create_order.pdf_path = invoice_filename
    db.session.commit()

    pdf_file = send_file(invoice_filename, as_attachment=True)
    return pdf_file











### Just takes an order from farmer and returns it in a better readable manner
@app.post('/format_order')
@app.input(OrderformattingIn)
@app.output(OrderformattingOut)
def format_order(json_data):
    
    order_desc = json_data['order_desc']
    formatted_order = nicely_formatted_order_gemini(order_desc)
    return {'formatted_order': formatted_order}



### List of counties that is returned to Watson
@app.get('/county_list')
@app.output(CountylistOut(many=True))
def get_countylist():
    counties = [
        {"name": "Baringo"},
        {"name": "Bomet"},
        {"name": "Bungoma"},
        {"name": "Busia"},
        {"name": "Elgeyo-Marakwet"},
        {"name": "Embu"},
        {"name": "Garissa"},
        {"name": "Homa Bay"},
        {"name": "Isiolo"},
        {"name": "Kajiado"},
        {"name": "Kakamega"},
        {"name": "Kericho"},
        {"name": "Kiambu"},
        {"name": "Kilifi"},
        {"name": "Kirinyaga"},
        {"name": "Kisii"},
        {"name": "Kisumu"},
        {"name": "Kitui"},
        {"name": "Kwale"},
        {"name": "Laikipia"},
        {"name": "Lamu"},
        {"name": "Machakos"},
        {"name": "Makueni"},
        {"name": "Mandera"},
        {"name": "Marsabit"},
        {"name": "Meru"},
        {"name": "Migori"},
        {"name": "Mombasa"},
        {"name": "Murang'a"},
        {"name": "Nairobi City"},
        {"name": "Nakuru"},
        {"name": "Nandi"},
        {"name": "Narok"},
        {"name": "Nyamira"},
        {"name": "Nyandarua"},
        {"name": "Nyeri"},
        {"name": "Samburu"},
        {"name": "Siaya"},
        {"name": "Taita-Taveta"},
        {"name": "Tana River"},
        {"name": "Tharaka-Nithi"},
        {"name": "Trans-Nzoia"},
        {"name": "Turkana"},
        {"name": "Uasin Gishu"},
        {"name": "Vihiga"},
        {"name": "Wajir"},
        {"name": "West Pokot"}
    ]
    return counties


### Supplier registration endpoint
@app.post('/reg_supplier')
@app.input(SupplierInSchema, location='json') 
def register_supplier(json_data):

    # Generate Supplier UUID "s_uuid" once 
    s_uuid = str(uuid.uuid4())

    # MySQL part 
    reg_supplier = Supplier(s_uuid=s_uuid, name=json_data['name'], phone=json_data['phone'], county=json_data['county'], email=json_data['email'], password=json_data['password'], location=json_data['location'])
    db.session.add(reg_supplier)
    try:
        db.session.commit()
        return jsonify({"message": "Supplier registered successfully", "status": "success"}), 200

    except Exception as e:
        db.session.rollback()  
        return jsonify({"message": "Could not add Supplier to MySQL database. Error: {}".format(str(e)), "status": "error"}), 400
    
    



#https://www.reddit.com/r/flask/comments/15lzkxx/i_have_tunneled_my_flask_app_to_ngrok_that_now_is/
#https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# my custom ngrok endpoint     
# https://f7123d742f2c9ee7.ngrok.app