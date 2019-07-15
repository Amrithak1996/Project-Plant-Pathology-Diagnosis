from flask import Blueprint,render_template,redirect,url_for,session,request,flash
from database import *
admin = Blueprint('admin',__name__)
@admin.route('/home/',methods=['get','post'])
def home():
	data={}
	return render_template('admin_home.html',data=data)
@admin.route('/logout/',methods=['get','post'])
def logout():
	data={}
	session.clear()
	return redirect(url_for('public.login'))
@admin.route('/view_users/',methods=['get','post'])
def view_users():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from user inner join login using(login_id)"
	user = select(q)
	data['user']=user
	return render_template('admin_view_users.html',data=data)
@admin.route('/view_uploaded_images/',methods=['get','post'])
def view_uploaded_images():
	data={}
	if 'action' in request.args:
		action = request.args['action']
		id = request.args['id']
	else:
		action=None
	q="select * from image inner join user using(user_id) inner join label using (label_id)"
	image = select(q)
	data['image']=image
	return render_template('admin_view_uploaded_images.html',data=data)


@admin.route('/admin_view_models/',methods=['get','post'])
def admin_view_models():
	data = {}
	q = "select * from model"
	model = select(q)
	data['model'] = model
	return render_template('admin_view_models.html',data=data)
@admin.route('/admin_view_labels/',methods=['get','post'])
def admin_view_labels():
	model_id = request.args['model_id']
	data = {}
	q = "select * from model inner join label using(model_id) where model_id='%s'" % model_id
	label = select(q)
	data['label'] = label
	return render_template('admin_view_labels.html',data=data)

@admin.route('/admin_add_precautions/',methods=['get','post'])
def admin_add_precautions():
	label_id = request.args['label_id']
	data = {}
	if "submit" in request.form:
		precatuions = request.form['precatuions']
		q = "update label set precatuions='%s' where label_id='%s'" % (precatuions,label_id)
		update(q)
		flash('success')
	q = "select * from model inner join label using(model_id) where label_id='%s'" % label_id
	label = select(q)
	data['label'] = label
	return render_template('admin_add_precautions.html',data=data)
