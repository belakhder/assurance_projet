from flask import flash,session
from main.models.profile import Profile
from utilities import postgres_connetion,close_postgres_connection
import uuid
import bcrypt
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def login(user_name,password,cur):
    """
    retrieve the credentiels make the comparison then allow the user to connect
    """
    check=False
    id=None
 
    psql=(
        f"""select id,password from users where user_name='{user_name}'""")
    cur.execute(psql)
    record=cur.fetchone()
    

    if not record:
        flash('nom utilisateur non valide!')
      
    else:
        id=record[0]
        password_record=record[1].tobytes() 

        if bcrypt.checkpw(password.encode('utf-8'),password_record):
            check=True
            flash("Connexion Réussi!")
        else:
            flash("Svp verifiez vos coordonnees et reessayer !")

    return [check,id]


def create_user(user,con,cur):
    """retrieves user data as an object 
        and inserts it into the database """

    values=(user.id,user.name,user.last_name,user.email,user.tel,user.user_name,user.password,user.user_type)

    cur.execute(
    """ insert into users  values (%s,%s,%s,%s,%s,%s,%s,%s)""",values)
    print(""" insert into users  values (%s,%s,%s,%s,%s,%s,%s,%s)""",values)
    con.commit()
def hash_string(password):
    hashed=b'h'
    password=(str(password)).encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed





# name,last_name,email,tel,user_name,password,user_type
def get_all_user(nb_page,cur):
    """
        get all users from database diplayed on pages
    """
    page_result=15
    offset=0
    offset=offset+page_result*(nb_page-1)
   
    psql_base=""" select name,last_name,email,tel,user_name,user_type,(
    select count(*)
    from users) as tot,id
    from users 
    """
  
    psql_page=f"""ORDER BY id
    OFFSET {offset} ROWS
    FETCH NEXT {page_result} ROWS ONLY"""
    psql=psql_base+psql_page
    cur.execute(psql)
    record=cur.fetchall()
    print(record)
    count=record[0][6]
    columns_names=['prénom','nom','email','tel',"nom d'utilisateur" ,"rôle",'Link']
  
  
    return count,page_result,columns_names,record

def search_user(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    if search_dict!={}:

        psql_base=""" select distinct * 
        from users 
        where """

        psql_where=""
        
        for (key,value) in search_dict.items() :
            psql_where= f"""{key}='{value}' and """+psql_where

        psql=psql_base+psql_where[:-4]+";"
        cur.execute(psql)
        record=cur.fetchall()

    else:
        record=None
    columns_names=['name','last_name','email','tel','user_name','password','user_type']
    #['prenom','nom','email','tel','Nom utilisateur','type utilisateur','nombre de resultat']
    
    return columns_names,record

def search_user_pages(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            psql_where= f"""{key}='{value}' and """+psql_where
        
      

        psql_base=f""" select distinct *,
        (select count(*) from users where {psql_where[:-4]}) as nb
        from users 
        where """

        offset=0
        page_result=5

        offset=offset+page_result*(nb_page-1)

        psql_page=f"""ORDER BY id
            OFFSET {offset} ROWS
            FETCH NEXT {page_result} ROWS ONLY"""
        psql=psql_base+psql_where[:-4]+psql_page
        cur.execute(psql)
        record=cur.fetchall()
        
        if record :
            count=record[0][8]
        else:
            record=None
            count=None
    else:
        record=None
        count=None
    columns_names=['prenom','nom','email','tel',"nom d'utilsateur","type d'utilisateur",'Link']
    
    return count,page_result,columns_names,record

def update_user_info(update_dict,id,con,cur):
    """
    update user table from database using information from dict
    """
    psql="update users set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()
def insert_settings(keys,values,con,cur):
    psql_settings=f""" insert into settings ({keys}) values {values};"""
    cur.execute(psql_settings)
    con.commit()
def update_settings_info(update_dict,id,con,cur):
    """
    update settings table from database using information from dict
    """
    psql="update settings set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()

def user_to_update(id,con,cur):
    """
    retrieve information from data base for a specified user
    """

    psql=f"""select name,last_name,email,tel,user_name,user_type from users where id='{id}'"""
    cur.execute(psql)
    record=cur.fetchall()
    user={'name':record[0][0],
        'last_name':record[0][1],
        'email':record[0][2],
        'tel':record[0][3],
        'user_name':record[0][4],
        'user_type':record[0][5]}
    return user


def search_all_user(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    record=None
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            psql_where= f"""{key}='{value}' and """+psql_where
        psql_base=f""" select distinct id,last_name,name,email,tel,user_name,user_type,
        (select count(*) from users where {psql_where[:-4]}) as nb
        from users 
        where """

        psql=psql_base+psql_where[:-4]
        record=cur.fetchall()
        cur.execute(psql)
        record=cur.fetchall()
    
    else:
        record=None

    
    return record