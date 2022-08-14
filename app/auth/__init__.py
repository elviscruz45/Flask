from flask import Blueprint
from . import views


auth=Blueprint("auth",__name__,url_prefix="/auth")

