from flask import Flask, request, jsonify, render_template, url_for, session, redirect
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from datetime import datetime, timezone

# https://stackoverflow.com/questions/68997414/sqlalchemy-exc-operationalerror-mysqldb-exceptions-operationalerror-1045
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/agridb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Farmer(db.Model):
    __tablename__ = 'farmers'
    farmerID =db.Column(db.Integer, primary_key = True)
    name =db.Column(db.String(500), nullable=False)
    phone =db.Column(db.String(100), nullable=False)
    location =db.Column(db.String(500), nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, name, phone, location, reg_date):
        self.name = name
        self.phone = phone
        self.location = location
        self.reg_date = reg_date


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
            db.session.add(insertfarmer)
            db.session.commit()
            return redirect('/')
        except: 
            return 'An Error occured registering the farmer.'
    else:
        return render_template('reg_farmer.html')


#Endpoint for creating and inserting a farmer into db using a JSON POST request.

@app.route('/reg_farmerJson', methods = ['POST'])
def reg_farmer_json():
    if request.is_json:
        data = request.get_json()
        name = data.get('name', None)
        phone = data.get('phone', None)
        location = data.get('location', None)
        f_regdate = datetime.now(timezone.utc)

        try:
            insertfarmer = Farmer(name, phone, location, f_regdate)
            db.session.add(insertfarmer)
            db.session.commit()
            return jsonify({"message": "Farmer added successfully", "status": "success"}), 200
        except:
            return jsonify({"message": "Request must be JSON", "status": "error"}), 400




#### @app.route('/submit_order', methods = ['GET','POST'])
### def create_order():
    ################# working on it

if __name__ == "__main__":
    app.run(debug=True)


#uninstall and reinstall python on pc to make sure no problem are happening here
    
#install pymysql also btw