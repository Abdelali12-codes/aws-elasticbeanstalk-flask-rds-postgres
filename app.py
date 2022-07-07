from flask import Flask,flash, request, render_template
from flask_sqlalchemy import SQLAlchemy 
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


db = SQLAlchemy(app)  


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

if __name__ == '__main__':  
   app.run(debug = True, host='0.0.0.0', port="8000")  
