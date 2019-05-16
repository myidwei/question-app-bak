# -*- coding: UTF-8 -*-
from flask import  Flask
from  flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://xiaowei:Admin19810919@liangxiaowei.mysql.rds.aliyuncs.com/gps_status'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    return app
