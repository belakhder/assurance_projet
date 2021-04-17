from flask import Blueprint,g,session
from main.services.service_contract import update_contract_,update_contract,add_contract,add_contract_,searching_contract_,get_searching_contract,download_csv,moneys_contract
from utilities import current_user
from auth import required_login,required_manager
contract=Blueprint('contract',__name__)

@contract.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
   
    g.current_user=current_user(id)
   
  else:
    g.current_user=None
  
@contract.route('/client/<id>/contract/<contract_id>' ,methods=['GET','POST'])
@required_login

def modify_client_contract(id,contract_id):
    
    return update_contract(id,contract_id)


@contract.route('/company/<id>/contract/<contract_id>' ,methods=['GET','POST'])
@required_login

def modify_company_contract(id,contract_id):
    
    return update_contract_(id,contract_id)

@contract.route('/client/<id>/contract' ,methods=['GET','POST'])
@required_login
def add_client_contract(id):

    return add_contract(id)
@contract.route('/company/<id>/contract' ,methods=['GET','POST'])
@required_login
def add_client_contract_(id):

    return add_contract_(id)

@contract.route('/search/contract' ,methods=['GET','POST'])
@required_login
def search_contract_():
  
    
    return searching_contract_()

@contract.route('/search/contrcat/result' ,methods=['GET'])
@required_login
def get_search_contract_():
    return get_searching_contract()


@contract.route('/csv/<file_name>' ,methods=['POST'])
@required_login
def dwlcsv(file_name):
    return download_csv(file_name)

@contract.route('/dashboard/con' ,methods=['GET','POST'])
@required_login
def dashbaord():
    
    return moneys_contract()