from flask import Flask, jsonify, flash, request, render_template
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

from flask_cors import CORS

import os

app = Flask(__name__)

if 'RDS_DB_NAME' in os.environ:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username=os.environ.get('RDS_USERNAME'),
        password=os.environ.get('RDS_PASSWORD'),
        host=os.environ.get('RDS_HOSTNAME'),
        port= '5432',
        database=os.environ.get('RDS_DB_NAME'),
    )
else:
    print("Hello The Rds db name does not exist")
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
        username='admin',
        password='admin1234',
        host='localhost',
        port='5432',
        database='user',
    )
app.config['SECRET_KEY'] = 'the random string'   # flask secret
app.config["JWT_SECRET_KEY"] = "super-secret"  #jwt secret this must be in env
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

xray_recorder.configure(service='flask')
XRayMiddleware(app, xray_recorder)


CORS(app)

db = SQLAlchemy(app)  
jwt = JWTManager(app)


class Users(db.Model):  
   id = db.Column('id', db.Integer, primary_key = True)  
   name = db.Column(db.String(150))  
   age = db.Column(db.String(50))     
  
   def __init__(self, name, age):  
      self.name = name 
      self.age = age  



@app.route('/')  
def message():  
      return "<html><body><h1>Hi, welcome to the website <a href='/form'> form </a> </h1></body></html>"  

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/hello')
def hello():
    return jsonify({'message':'Hello Dear user'}), 200  

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
      
          return "Login via the login Form"
     
    if request.method == 'POST':

        user = Users(request.form['name'], request.form['age'])
        
        db.session.add(user)  
        db.session.commit()  
        flash('Record was successfully added')

        return f"Done!!"


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route('/profile')
@jwt_required()
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body


if __name__ == '__main__':  
   app.run(debug = True, host='0.0.0.0', port="8000")  
