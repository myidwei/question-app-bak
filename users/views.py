from users import users
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import json
from models import *
from database import *
import random
import string
import time, datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
from commons import *

def is_login():
    user = session.get('login_user')
    return user != None

# def send_mail(email,subject,content):
#     encoding = 'utf-8'
#     mail = MIMEText(content.encode(encoding),'plain',encoding)
#     mail['Subject'] = Header(subject,encoding)
#     mail['From'] = "wattsappbronx@outlook.com"
#     mail['To'] = email
#     mail['Date'] = formatdate()
#     smtp = smtplib.SMTP("smtp.office365.com",587)
#     smtp.set_debuglevel(1)
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.ehlo()
#     smtp.login("wattsappbronx@outlook.com", "wattsapp_123") 
#     smtp.sendmail("wattsappbronx@outlook.com", email, mail.as_string()); 
#     smtp.quit()

def send_mail(email,subject,content):
    encoding = 'utf-8'
    mail = MIMEText(content.encode(encoding),'plain',encoding)
    mail['Subject'] = Header(subject,encoding)
    mail['From'] = "myidwei@qq.com"
    mail['To'] = email
    mail['Date'] = formatdate()
    smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
    smtp.login("myidwei@qq.com", "veuqwuizssqfbidf") 
    smtp.sendmail("myidwei@qq.com", email, mail.as_string()); 
    smtp.quit()

@users.route('/reg')
def reg_page():
    return users.send_static_file('reg.html')

@users.route('/list')
def user_list():
    if not is_login():
        return redirect(url_for('Users.login_page'))
    return users.send_static_file('user_list.html')

@users.route('/user_add')
def user_add():
    return users.send_static_file('user_add.html')


@users.route('/get_user_list')
def get_user_list():
    email = session.get("login_user")
    if email == None:
        return failed(-1,'User not login')
    rows = db.session.query(RegUser).filter(RegUser.email != email).all()
    return success(convert_dict(rows))
    

@users.route('/update_question')
def update_question():
    return users.send_static_file('update_question.html')

@users.route('/forget')
def forget_password():
    return users.send_static_file('forget.html')

@users.route('/login')
def login_page():
    return users.send_static_file('login.html')

@users.route('/change_password')
def change_password_page():
    if not is_login():
        return redirect(url_for('Users.login_page'))
    return users.send_static_file('change_password.html')

@users.route('/logout')
def logout():
    session.clear()
    return users.send_static_file('login.html')

@users.route('/user_info')
def user_info():
    email = session.get("login_user")
    if email == None:
        return failed(403,'User not login')
    row = db.session.query(RegUser).filter_by(email=email).first()
    return success(row.column_dict())

@users.route('/index')
def index_page():
    if is_login():
        return users.send_static_file('index.html')
    else:
        return redirect(url_for('Users.login_page'))

@users.route('/do_login',methods=["POST"])
def do_login():
    data = json.loads(request.get_data(as_text=True))
    email = data['email']
    password = data['password'];
    row = db.session.query(RegUser).filter_by(email=email).filter_by(password=password).first()
    if row == None:
        return failed(-1,'Login failed!')
    session['login_user'] = row.email
    return success(True)

@users.route('/do_change_password',methods=["POST"])
def do_change_password():
    data = json.loads(request.get_data(as_text=True))
    email = session.get("login_user")
    if email == None:
        return users.send_static_file('login.html')
    old_password = data['old_password']
    new_password = data['new_password']
    row = db.session.query(RegUser).filter_by(email=email).filter_by(password=old_password).first()
    if row == None:
        return failed(-1,'Old password error!')
    db.session.query(RegUser).filter_by(email=email).update({'password':new_password,'status':2})
    db.session.commit()
    return success(True)

@users.route('/do_reg',methods=["POST"])
def do_reg():
    user = user_info()
    if user == None:
        return failed(403,'Need Login')
    
    data = json.loads(request.get_data(as_text=True))
    email = data['email']
    row = db.session.query(RegUser).filter_by(email=email).first()
    if row != None:
        return failed(-1,'Email already registered!')
    passwd = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    content = "Your register email:" + email + ", your password:" + passwd;
    send_mail(email,"Your register information",content);
    user = RegUser(email=email,first_name=data['first_name'],last_name=data['last_name'],level=data['level'],password=passwd,status=1,reg_time=int(time.time()))
    db.session.add(user)
    db.session.commit()
    return success(user.id)

@users.route('/do_forget',methods=["POST"])
def do_forget():
    data = json.loads(request.get_data(as_text=True))
    email = data['email']
    row = db.session.query(RegUser).filter_by(email=email).first()
    if row == None:
        return failed(-1,'Email not registered!')

    content = "Your register email:" + email + ", your password:" + row.password;
    send_mail(email,"Forget your password",content);
    
    return success(True)

@users.route('/del',methods=["POST"])
def del_user():
    email = session.get("login_user")
    if email == None:
        return failed(403,'User not login')
    data = json.loads(request.get_data(as_text=True))
    id = data['id']
    row = db.session.query(RegUser).filter_by(id=id).first()
    if row == None:
        return failed(-1,'User not found!')
    db.session.delete(row)
    db.session.commit()
    return success(True)
