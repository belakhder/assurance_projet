import json
from flask.globals import session

from werkzeug.utils import redirect


# def test_index(app, client):
#     res = client.get('/home')
#     print(res.get_data(as_text=True))
#     assert res.status_code == 200
#     expected = {'hello': 'world'}
    #assert expected == json.loads(res.get_data(as_text=True))




# def test_index2(app, client):
#     res = client.post('/')
#     print(res.get_data(as_text=True))
#     assert res.status_code == 405
#     expected = {'hello': 'world'}


def test_login_success(app, client,captured_templates):
    data={'user_name':'127','password':'Fattouh1990','submit': 'Se connecter'}

    res = client.post('/home',data = data,follow_redirects=True)
    assert len(captured_templates) == 2
    template, context = captured_templates[1]
    assert template.name=='search/search_client.html' 


    assert res.status_code == 200

def test_login_user_name_failure(app, client,captured_templates):
    data={'user_name':'414','password':'Fattouh1990','submit': 'Se connecter'}

    res = client.post('/home',data = data,follow_redirects=True)
    print(res.data)
    assert b'nom utilisateur non valide' in res.data
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name=='page_acceuil.html' 
    assert res.status_code == 200

def test_login_password_failure(app, client,captured_templates):
    data={'user_name':'127','password':'fattouh1990','submit': 'Se connecter'}

    res = client.post('/home',data = data,follow_redirects=True)
    print(res.data)
    assert b'Svp verifiez vos coordonnees et reessayer !' in res.data
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name=='page_acceuil.html' 
    assert res.status_code == 200
    
def test_subscription_client(app, client):

    data_log={'user_name':'127','password':'Fattouh1990','submit': 'Se connecter'}
    client.post('/home',data = data_log,follow_redirects=False)
    data={'company_name': 'dfdfff', 'company_registration_nb': 'xd14dfd', 'client_type':'Client', 'company_email':'fbewxcl1414a@live.fr', 'phone':'41474774', 'full_number':'+21641474774','line1':'rue printemps', 'line2': 'bn', 'city':'agba', 'state': 'tunis', 'postal_code':'2011','country':'tunisie','contract_type':'type 1','price':'80','start_date':'2021-01-20','end_date':'2021-01-28','nb_inst':'14','payment_amount':'80','payment_mode':'Cash','nb_bank_check':'','transaction_number':'','card_number': '', 'payor_last_name':'','payor_name':''}
    res = client.post('/search/company',data = data,follow_redirects=True)
    
    print(res.data)
    assert res.status_code == 200



