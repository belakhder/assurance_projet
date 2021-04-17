
from flask import Blueprint,g,session,jsonify,render_template
from auth import required_login,required_manager
from utilities import current_user
from main.services.service_payments import show_payments,inst_update,inst_payment,search_result,searching_payments,download_csv
payment=Blueprint('payment',__name__)

@payment.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@payment.route('/client/<id>/contract/<contract_id>/payments' ,methods=['GET','POST'])

def show_all_payments(id,contract_id):
    return show_payments(id,contract_id)



@payment.route('/client/<id>/contract/<contract_id>/payments/payment' ,methods=['GET','POST'])

def paye_payments(id,contract_id):
    return inst_update(id,contract_id)

@payment.route('/client/<id>/contract/<contract_id>/payments/<inst_id>' ,methods=['GET','POST'])
def inst_payments(id,contract_id,inst_id):
    return  inst_payment(id,contract_id,inst_id)


@payment.route('/search/payments' ,methods=['GET','POST'])
@required_login
def search_payments():
  
    return searching_payments()

@payment.route('/search/payments/result' ,methods=['GET','POST'])
@required_login
def search_result_():
    return search_result()

@payment.route('/payment_csv/<file_name>' ,methods=['POST'])
@required_login
def dwlcsvp(file_name):
    return download_csv(file_name)
