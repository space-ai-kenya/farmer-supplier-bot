from flask import Flask
from flask_cors import CORS
from flask import request, jsonify, render_template, url_for, session, redirect, send_file
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import re

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


# APIFlask configuration 

app = Flask(__name__,static_folder='static',template_folder='templates')
CORS(app, resources={r"*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})




@app.route('/<string:phone_no>/add_multiple_cows', methods=['GET'])
def add_multiple_cows(phone_no):
    # Define a regular expression pattern for a valid Kenyan phone number format
    kenyan_phone_pattern = re.compile(r'^(?:\+254|0)?7\d{8}$')  # Accepts both "+254" and "0" as prefixes
    
    # Check if the phone number matches the expected format
    if not kenyan_phone_pattern.match(phone_no):
        return "Invalid Kenyan phone number format", 400  # Return a 400 Bad Request status code
    
    if request.method == 'GET':
        context = {'phone_no': phone_no}  # Include phone_no in the context dictionary   
        # Serve HTML form with the context dictionary
        return render_template('farm_card/cows.html', **context)

    

if __name__ == "__main__":
    app.run(debug=True, port=4046)