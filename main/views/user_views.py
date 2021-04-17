
from flask import Blueprint,session,g,render_template,redirect
from main.services.service_user import logout,login_user,subscription,display_all_user,searching_user_,search_user_pages,get_searching_user,update_users_info,insert_settings_,update_settings
from utilities import current_user
from auth import required_login
user=Blueprint('user',__name__)

@user.before_request
def current_user_():
  if 'user' in session:
    id=session['user']
    g.current_user=current_user(id)
  else:
    g.current_user=None

@user.route('/home' ,methods=['GET','POST'])
def login_users():
  

  return login_user()

@user.route('/home/user' ,methods=['GET','POST'])
@required_login
def subscribe_users():
  
  return subscription()

@user.route('/logout' ,methods=['GET','POST'])
def deconnection():
  
  return logout()
@user.route('/home/users' ,methods=['GET','POST'])
@required_login
def get_all_users():
    return display_all_user()

@user.route('/search/users' ,methods=['GET','POST'])
@required_login
def search_user_():
    return searching_user_()

@user.route('/search/users/result' ,methods=['GET'])
@required_login
def get_search_user_():
    return get_searching_user()


@user.route('/user/<id>/information' ,methods=['GET','POST'])
@required_login
def modify_user(id):
  
  return update_users_info(id)

@user.route('/settings' ,methods=['GET','POST'])
@required_login
def insert_settings():
   
  return insert_settings_()
@user.route('/settings/1' ,methods=['GET','POST'])
@required_login
def modify_settings():
   
  return update_settings()

@user.route('/dashboard' ,methods=['GET','POST'])
@required_login
def dash():
    return render_template('dash.html')