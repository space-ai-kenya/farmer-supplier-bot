from apiflask import APIFlask
from flask_cors import CORS
from flask import request, jsonify, render_template, url_for, session, redirect, send_file
import os
from datetime import datetime, timezone
from dotenv import load_dotenv


load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


# APIFlask configuration 

app = APIFlask(__name__, title='', version='', static_folder='static',template_folder='templates')
CORS(app, resources={r"*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})



@app.route('/', methods=['GET'])
def register_farmer_form():
    if request.method == 'GET':
        # Serve HTML form
        return render_template('farmer_supplier/index.html')
    

if __name__ == "__main__":
    app.run(debug=True, port=4046)