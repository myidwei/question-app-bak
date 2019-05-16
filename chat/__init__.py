from flask import Blueprint
import os
chat = Blueprint("Chat",__name__,static_folder='static')
from chat import views