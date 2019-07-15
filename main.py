from flask import Flask,render_template,redirect,url_for,session,request,flash
import database as db
app = Flask(__name__)
app.secret_key ='pearl_ready'
from public import public
app.register_blueprint(public)
from admin import admin
app.register_blueprint(admin,url_prefix='/admin')
from api import api
app.register_blueprint(api,url_prefix='/api')
app.run(debug=True,port=5003,host="192.168.43.101")


 