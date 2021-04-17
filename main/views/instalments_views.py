
from flask import Blueprint,g,session,jsonify,render_template
import psycopg2
from auth import required_login,required_manager
from utilities import current_user
from utilities_client import search_client
from main.services.service_instalments import inst_payment_,show_instalments,inst_update,inst_payment,search_result,searching_instalments,show_instalments_company
instalment=Blueprint('instalment',__name__)

@instalment.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None
@instalment.route('/client/<id>/contract/<contract_id>/instalments' ,methods=['GET','POST'])

def show_all_instalments(id,contract_id):
    return show_instalments(id,contract_id)

@instalment.route('/company/<id>/contract/<contract_id>/instalments' ,methods=['GET','POST'])

def show_all_instalments_(id,contract_id):
    return show_instalments_company(id,contract_id)

@instalment.route('/client/<id>/contract/<contract_id>/instalments/payment' ,methods=['GET','POST'])

def paye_instalments(id,contract_id):
    return inst_update(id,contract_id)



@instalment.route('/client/<id>/contract/<contract_id>/instalments/<inst_id>' ,methods=['GET','POST'])
def inst_payments(id,contract_id,inst_id):
    return  inst_payment(id,contract_id,inst_id)

@instalment.route('/company/<id>/contract/<contract_id>/instalments/<inst_id>' ,methods=['GET','POST'])
def inst_payments_(id,contract_id,inst_id):
    return  inst_payment_(id,contract_id,inst_id)



@instalment.route('/search/instalments' ,methods=['GET','POST'])
@required_login
def search_instalments():
  
    return searching_instalments()

@instalment.route('/search/instalments/result' ,methods=['GET','POST'])
@required_login
def search_result_():
  
    return search_result()

def get_client_id(id,con):
    """get client id """
    cur=con.cursor()
    cur.execute(f"""select * from clients where id={id}""")
    record=cur.fetchone()
    return record

@instalment.context_processor
def context_processor():


    return dict(get_client_id=get_client_id)