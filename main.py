from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime
import json
# from flask_mail import Mail

# import os

local_server=True
c=open('templates\\config.json', 'r') 
params = json.load(c)['params']
# for key, value in params.items():
#     print(f'{key} is the key n {value} is the value.\n')
# print(params['local_uri'])

pagenumber=0
app=Flask(__name__)
app.secret_key='my-secret-key'


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['prod_uri']
db=SQLAlchemy(app)

class Contacts(db.Model):
    serial_no=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(400), unique=True)
    email=db.Column(db.String(400), unique=True)
    phone=db.Column(db.String(15), unique=True)
    message=db.Column(db.String(4000), unique=True)
    date=db.Column(db.Date, unique=True)

class Posts(db.Model):
    serial_no=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(400), unique=True)
    slug=db.Column(db.String(400), unique=True)
    content=db.Column(db.String(15), unique=True)
    date=db.Column(db.Date, unique=True)
    author=db.Column(db.String(1000))



@app.route('/')
def home():
    all_posts=Posts.query.all()
    return render_template('index.html', params=params, all_post_var=all_posts, pagestart=0)

@app.route('/<string:page_slug>', methods=['GET'])
def post_page(page_slug):
    all_posts=Posts.query.all()
    total_post=len(all_posts)
    total_post_possible=(int(page_slug)+1)*params['no_of_pages']
    if page_slug == '0':
        return render_template('index.html', params=params, all_post_var=all_posts, pagestart=0)
    if (total_post_possible-total_post) <= params['no_of_pages'] and (total_post_possible-total_post)>=0:
        return render_template('lastpage.html', pagestart=int(page_slug), params=params, all_post_var=all_posts, total_post=total_post)
    else:
        return render_template('middlepage.html', pagestart=int(page_slug), params=params, all_post_var=all_posts)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    # print(f'{Posts.serial_no} is the serial no')
    for item in Posts.query:
        if item.slug == post_slug:
            post=item
            break
    # print(type(post))
    return render_template('post.html', params=params, post=post)

@app.route('/about')#,  params=params)
def printabout():
    # author='Diksha Wali'
    return render_template('about.html',  params=params)

@app.route('/contact', methods=['GET', 'POST'])#,  params=params)
def printcontact():
    # author='Diksha Wali' 
    if request.method=='POST':
        # add entry to the database
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')

        entry=Contacts(name=name, email=email, phone=phone, message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
        # mail.send_message(f'New message from {name}', 
        #                     sender=email, 
        #                     recipients=params['mail_un'] ,
        #                     body = message + '\n' + phone)

    return render_template('contact.html', params=params)

@app.route('/post')#, params=params)
def printpost():
    # author='Diksha Wali'
    return render_template('post.html', params=params)

@app.route('/dashboard', methods=['GET', "POST"])
def dashboard():
    mainpage_post=Posts.query.all()
    if 's_user' in session and session['s_user']==params['admin_username']:
        return render_template('dashboard.html', params=params, html_post=mainpage_post)

    if request.method=='POST':
        username=request.form.get('Username')
        password=request.form.get('password')
        if (username==params['admin_username'] and password==params['admin_password']):
            # set the session variable
            session['s_user']=username
        return render_template('bad request', params=params)

@app.route('/edit/<string:s_no>', methods=['GET', "POST"])
def edit_fun(s_no):
    main_srno=s_no
    if 's_user' in session and session['s_user']==params['admin_username']:
        if request.method=='POST':
            main_post=Posts.query.filter_by(serial_no=s_no).first()
            main_post.title=request.form.get('title')
            main_post.slug=request.form.get('slug')
            main_post.content=request.form.get('content')
            main_post.date=datetime.now()
            db.session.commit()
    return render_template('edit.html', params=params, html_srno=main_srno)        

    



c.close()

app.run(debug=True)