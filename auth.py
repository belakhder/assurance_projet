from os import environ
from flask import request,session,flash,render_template,g,url_for,redirect
from functools import wraps
from urllib.request import urlopen




class AuthError(Exception):
    '''A standardized way to communicate auth failure modes'''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code



def required_login(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if 'user' not in  session:
            flash('please login')
            return render_template('page_acceuil.html')
        return f(*args,**kwargs)
    return wrapper


def required_manager(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if 'user' in  session:
            if g.current_user[1] !='Manager':
                flash('you are not authorized !')
                
                return redirect(url_for('client.display_client',id=session['client_id'],contract_id=session['contract_id']))
        return f(*args,**kwargs)
    return wrapper   
         
def required_manager_(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if 'user' in  session:
            if g.current_user[1] !='Manager':
                flash('you are not authorized !')
                
                return redirect(url_for('client.display_company',id=session['client_id'],contract_id=session['contract_id']))
        return f(*args,**kwargs)
    return wrapper 