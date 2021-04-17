from flask import Flask
from config import *

from flask_mail import Mail
from flask_toastr import Toastr



def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config['SECRET_KEY']='hjb,n'
    app.config['MAIL_DEBUG'] = MAIL_DEBUG
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
    mail = Mail(app)
    toastr = Toastr(app)
    return app

