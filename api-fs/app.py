from apiflask import APIFlask
from flask import request, jsonify, render_template, url_for, session, redirect
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from datetime import datetime, timezone
import requests as rq
from dotenv import load_dotenv

# ------- my local imports
from database.models import Farmer
from schema.farmer_schema import FarmerInSchema,FarmerOutSchema

load_dotenv()

# https://stackoverflow.com/questions/68997414/sqlalchemy-exc-operationalerror-mysqldb-exceptions-operationalerror-1045
app = APIFlask(__name__, title='', version='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:mypassword@mysql_db:3306/agridb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Endpoint for creating and inserting a farmer into db from a form using POST
@app.route('/', methods=['GET','POST'])
def Reg_FarmerForm():
    if request.method == 'POST':
        f_name = request.form.get('name')
        f_phone = request.form.get('phone')
        f_location = request.form.get('location')
        f_regdate = datetime.now(timezone.utc)
        insertfarmer = Farmer(f_name, f_phone, f_location, f_regdate)

        try:
            # db.session.add(insertfarmer)
            # db.session.commit()
            return redirect('/')
        except: 
            return 'An Error occured registering the farmer.'
    else:
        return render_template('reg_farmer.html')


@app.post('/reg_farmerJson')
@app.input(FarmerInSchema)  
def reg_farmer_json(json_data):

    data = json_data
    name = data.get('Name', None)
    phone = data.get('Phone', None)
    location = data.get('Location', None)
    f_regdate = datetime.now(timezone.utc)

    print(name, phone, location)

    # try:
    #     insertfarmer = Farmer(name, phone, location, f_regdate)
    #     db.session.add(insertfarmer)
    #     db.session.commit()
    #     return jsonify({"message": "Farmer added successfully", "status": "success"}), 200
    # except:
    #     return jsonify({"message": "Request must be JSON", "status": "error"}), 400

    return {'message': 'created'}




#### @app.route('/submit_order', methods = ['GET','POST'])
### def create_order():
    ################# working on it



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


#uninstall and reinstall python on pc to make sure no problem are happening here
    
#install pymysql also btw