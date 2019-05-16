import json
from models import *
from database import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
def success(obj):
    return jsonify({'code':0,'msg':'success','data':obj}), 200

def failed(code,msg):
    return jsonify({'code':code,'msg':msg}), 200

def user_info():
    email = session.get("login_user")
    if email == None:
        return None
    row = db.session.query(RegUser).filter_by(email=email).first()
    return row

def get_tags(id):
    rows = db.session.query(QuestionTagRel).filter_by(question_id=id).all()
    tag_ids = []
    for item in rows:
        tag_ids.append(item.tag_id)
    tags = db.session.query(Tags).filter(Tags.id.in_(tag_ids)).all()
    items = []
    for tag in tags:
            items.append(tag.name)
    return items

def get_tags_info(id):
    rows = db.session.query(QuestionTagRel).filter_by(question_id=id).all()
    tag_ids = []
    for item in rows:
        tag_ids.append(item.tag_id)
    tags = db.session.query(Tags).filter(Tags.id.in_(tag_ids)).all()
    items = []
    for tag in tags:
            items.append(tag.column_dict())
    return items

def get_tag_by_name(name):
    rows = db.session.query(Tags).filter_by(name=name).first()
    return rows

def get_category_list():
    return db.session.query(Category).all();

def get_tag_list():
    return db.session.query(Tags).all();

def convert_dict(rows):
    ret = []
    for item in rows:
        ret.append(item.column_dict())
    return ret