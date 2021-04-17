from flask import Blueprint,g
from auth import required_login
from main.services.service_address import *
from utilities import current_user
address=Blueprint('address',__name__)

@address.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@address.route('/client/<id>/address/<address_id>' ,methods=['GET','POST'])
@required_login
def modify_client_address(id,address_id):
    return update_address(id,address_id)
@address.route('/company/<id>/address/<address_id>' ,methods=['GET','POST'])
@required_login
def modify_client_address_(id,address_id):
    return update_address_(id,address_id)