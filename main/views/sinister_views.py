

from flask import Blueprint,g,session
from main.services.service_sinister import *
from utilities import current_user
from auth import required_login
sinister=Blueprint('sinister',__name__)

@sinister.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None
@sinister.route('/client/<id>/contract/<contract_id>/sinister' ,methods=['GET','POST'])
@required_login
def add_sinister(id,contract_id):

    return add_one_sinister(id,contract_id)

@sinister.route('/company/<id>/contract/<contract_id>/sinister' ,methods=['GET','POST'])
@required_login
def add_sinister_(id,contract_id):

    return add_one_sinister_(id,contract_id)   

@sinister.route('/client/<id>/sinister/<sinister_id>' ,methods=['GET','POST'])
@required_login
def modify_sinister(id,sinister_id):
    
    return update_sinister(id,sinister_id)



@sinister.route('/company/<id>/sinister/<sinister_id>' ,methods=['GET','POST'])
@required_login
def modify_sinister_(id,sinister_id):
    
    return update_sinister_(id,sinister_id)

@sinister.route('/search/sinisters' ,methods=['GET','POST'])
@required_login
def search_sinisters():
   
    return searching_sinisters()

@sinister.route('/search/sinisters/result' ,methods=['GET'])
@required_login
def search_result_():
  
    return search_result()

