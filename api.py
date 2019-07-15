from flask import Blueprint,render_template,redirect,url_for,session,request,flash
from database import *
import demjson
from keras.models import load_model
from keras.backend import clear_session
from core import load_image
import numpy as np
import uuid


api = Blueprint('api',__name__)

@api.before_request
def beep():
	import winsound
	winsound.Beep(2500,100)

@api.route('/register/',methods=['get','post'])
def register():
	data={}
	username = request.args['username']
	password = request.args['password']
	first_name = request.args['first_name']
	last_name = request.args['last_name']
	age = request.args['age']
	email = request.args['email']
	phone = request.args['phone']
	gender = request.args['gender']
	q = "insert into login (username,password,login_type,login_status)values('%s','%s','%s','%s')" % (username,password,'user','active')
	login_id = insert(q)
	q = "insert into user (login_id,first_name,last_name,age,gender,email,phone)values('%s','%s','%s','%s','%s','%s','%s')" % (login_id,first_name,last_name,age,gender,email,phone)
	insert(q)
	data['status'] = 'success'
	return demjson.encode(data)



@api.route('/login/',methods=['get','post'])
def login():
	data={}
	data.update(request.args)
	username = request.args['username']
	password = request.args['password']
	q = "select * from login inner join user using(login_id) where username='%s' and password='%s'" % (username,password)
	res = select(q)
	if(len(res) > 0):
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	return  demjson.encode(data)
@api.route('/get_model')
def get_classess():
	data= {}
	q = "select * from model"
	res = select(q)
	data['data'] = res
	data['status'] = 'success'
	return demjson.encode(data)


@api.route('/upload_image/',methods=['get','post'])
def upload_image():
	data={}
	image = request.files['image']
	login_id = request.form['login_id']
	filename = "static/uploads/" + str(uuid.uuid4()) + "." + "jpg"
	image.save(filename)
	model_id = request.form['model_id']
	q = "select * from model where model_id='%s'" % model_id
	res = select(q)
	clear_session()
	model = load_model(res[0]['model_path'])
	# filename = "Data/Tomato_Bacterial_spot/00416648-be6e-4bd4-bc8d-82f43f8a7240___GCREC_Bact.Sp 3110.JPG"
	image = load_image(filename,(224,224))
	# print(image)
	# if image:
	image = np.expand_dims(image, axis=0)
	result = model.predict(image)
	index = np.argmax(result) 
	q = "select * from label where model_id='%s'" % model_id
	res = select(q)
	q = "insert into image(user_id,file_path,label_id)values((select user_id from user where login_id='%s'),'%s','%s')" % (login_id,filename,res[index]['label_id'])

	data['data'] = [res[index]]
	data['status'] = 'success' 
	# else:
	# 	data['status'] = 'failed'
	return demjson.encode(data)
# @api.route('/take_action')
# def take_action():
# 	q="""SELECT *,TIME(DATE_ADD(NOW(), INTERVAL -1 HOUR)), TIME(NOW()) FROM notification WHERE date(notification_date)=CURDATE() 
# 	AND TIME(notification_date) BETWEEN TIME(DATE_ADD(NOW(), INTERVAL -2 HOUR)) AND TIME(NOW()) AND   notification_status='pending'"""
# 	res=select(q)
# 	if not res:
# 		moisture=request.args['moisture']
# 		q="insert into notification (notification_date,notification_status,moisture) values(now(),'pending','%s')"%moisture
# 		insert(q)
# 	data={}
# 	data['status']='success'
# 	return demjson.encode(data)
# @api.route('/get_notification')
# def get_notifications():
# 	q="select * from notification where notification_status='pending'"
# 	res=select(q)
# 	q="update notification set notification_status='viewed'"
# 	update(q)
# 	data={}
# 	data['data']=res
# 	data['status']='success'
# 	return demjson.encode(data)
