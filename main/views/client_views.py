from math import pi
from flask import current_app,flash
from utilities_sinister import sinister_to_update
from jinja2 import Template
import datetime

from flask_mail import Mail
from flask_mail import Message
from config import *
import os

from itsdangerous import URLSafeTimedSerializer,SignatureExpired


from flask import Blueprint,g,session,jsonify,json,render_template
from auth import required_login,required_manager
from utilities import current_user,envoi_mail_html
from utilities_client import search_fiche_client
from main.services.service_company import display_all_companies,display_one_company,update_companies_info,searching_company_,get_searching_company
from main.services.service_client import searching_client,client_subscription,display_one_client,update_clients_info,display_all_client,searching_client_,get_searching_client,download_csv,company_subscription,error_422_handler_search

client=Blueprint('client',__name__)

@client.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@client.route('/search' ,methods=['GET','POST'])
@required_login
def search_client_():
  
    print(g.current_user)
    return searching_client_()

@client.route('/search/result' ,methods=['GET'])
@required_login
def get_search_client_():
    return get_searching_client()

@client.route('/search/company' ,methods=['GET','POST'])
@required_login
def search_company_():
  
    print(g.current_user)
    return searching_company_()

@client.route('/search/company/result' ,methods=['GET'])
@required_login
def get_search_company_():
    return get_searching_company()

@client.route('/client' ,methods=['GET','POST'])
@required_login
def subscription():
    
    return client_subscription()

@client.route('/company' ,methods=['GET','POST'])
@required_login
def subscription_company():
    
    return company_subscription()
@client.route('/client/<id>/contracts/<contract_id>' ,methods=['GET','POST'])
@required_login
def display_client(id,contract_id):
    return display_one_client(id,contract_id)

@client.route('/company/<id>/contracts/<contract_id>' ,methods=['GET','POST'])
@required_login
def display_company(id,contract_id):
    return display_one_company(id,contract_id)

@client.route('/client/<id>/information' ,methods=['GET','POST'])
@required_login
def modify_client(id):
    return update_clients_info(id)

@client.route('/clients' ,methods=['GET','POST'])
@required_login
def get_all_clients():
    return display_all_client()

@client.route('/companies' ,methods=['GET','POST'])
@required_login
def get_all_companies():
    return display_all_companies()

@client.route('/csv/<file_name>' ,methods=['POST'])
@required_login
def dwlcsv(file_name):
    return download_csv(file_name)

@client.context_processor
def utility_processor():
  return dict(sinister_to_update=sinister_to_update)

@client.route('/company/<id>/information' ,methods=['GET','POST'])
@required_login
def modify_client_(id):
    return update_companies_info(id)


@client.route('/confirm_subscription')
def confirm_subscription():

    with current_app.app_context():
        mail = Mail()
        
        msg = Message("Hello",
                    sender="belakhder.fathi@gmail.com",
                    recipients=["fbelakhdhar@live.fr"])
        mail.send(msg)
    return jsonify({'message':'congratulations your membership is a valid one'})


@client.errorhandler(422)
def error_422(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@client.errorhandler(422)
def error_400(error):
    flash('error')
    return  render_template("client/souscription_client.html",now=str(datetime.datetime.now().date()))


@client.errorhandler(404)
def error_400(error):
    return error_422_handler_search()

    