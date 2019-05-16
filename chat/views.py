from chat import chat
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
import json
from models import *
from database import *
import random
import string
import time, datetime
from commons import *
from app import *

@chat.route('/customer')
def customer_page():
    return chat.send_static_file('customer.html')

@chat.route('/service')
def service_page():
    return chat.send_static_file('service.html')
