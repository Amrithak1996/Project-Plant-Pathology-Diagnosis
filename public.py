from flask import Blueprint,render_template,redirect,url_for,session,request,flash
from database import *
public = Blueprint('public',__name__)
@public.route('/',methods=['get','post'])
def home():
	data={}
	return render_template('public_home.html',data=data)
@public.route('/login/',methods=['get','post'])
def login():
	data={}
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="select * from login where username='%s' and password='%s'" % (username,password)
		res = select(q)
		if len(res) > 0:
			session['login_id']=res[0]['login_id']
			if res[0]['login_type'] == 'public':
				return redirect(url_for('public.home'))
			if res[0]['login_type'] == 'admin':
				return redirect(url_for('admin.home'))
			if res[0]['login_type'] == 'user':
				return redirect(url_for('user.home'))
		else:
			flash('login_failed.Try Again.')
	return render_template('public_home.html',data=data)
@public.route('/register/',methods=['get','post'])
def register():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from login"
	login = select(q)
	data['login']=login
	if 'add_user' in request.form:
		username=request.form['username']
		password=request.form['password']
		login_type='user'
		q="insert into login(username,password,login_type,login_status)values('%s','%s','%s','active')" % (username,password,login_type)
		login_id = insert(q)
		first_name=request.form['first_name']
		last_name=request.form['last_name']
		age=request.form['age']
		gender=request.form['gender']
		email=request.form['email']
		phone=request.form['phone']
		q = "insert into user(login_id,first_name,last_name,age,gender,email,phone)VALUES('%s','%s','%s','%s','%s','%s','%s')" % (login_id,first_name,last_name,age,gender,email,phone) 
		insert(q)
		flash('Success')
	return render_template('public_register.html',data=data)
