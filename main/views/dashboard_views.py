from flask import Blueprint,g,session
from main.services.service_dashbord import moneys_contract
from utilities import current_user
from auth import required_login,required_manager
dashboard=Blueprint('dashboard',__name__)


@dashboard.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
   
    print(current_user(id))
    g.current_user=current_user(id)
    print(g.current_user)
  else:
    g.current_user=None

@dashboard.route('/dashboard/con' ,methods=['GET','POST'])
@required_login
def dashboard_display():
    
    return moneys_contract()