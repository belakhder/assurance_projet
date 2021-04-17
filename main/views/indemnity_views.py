

from flask import Blueprint,session,g
from main.services.service_indemnity import update_indemnity_,update_indemnity,searching_indemnities,search_result
from auth import required_login,required_manager,required_manager_
from utilities import current_user
indemnity=Blueprint('indemnity',__name__)

@indemnity.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
   
    print(current_user(id))
    g.current_user=current_user(id)
    print(g.current_user)
  else:
    g.current_user=None


@indemnity.route('/client/<id>/indemnity/<indemnity_id>' ,methods=['GET','POST'])
@required_login
@required_manager
def modify_indemnity(id,indemnity_id):
    
    
    return update_indemnity(id,indemnity_id)



@indemnity.route('/company/<id>/indemnity/<indemnity_id>' ,methods=['GET','POST'])
@required_login
@required_manager_
def modify_indemnity_(id,indemnity_id):
    print('hee')
    
    return update_indemnity_(id,indemnity_id)

@indemnity.route('/search/indemnities' ,methods=['GET','POST'])
@required_login
def search_indemnities():
  
    return searching_indemnities()


@indemnity.route('/search/indemnities/result' ,methods=['GET','POST'])
@required_login
def search_result_():
  
    return search_result()
