from main.models.sinister import Sinister
from utilities import postgres_connetion,close_postgres_connection
import uuid
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def add_sinister(sinister,extern_id,id,contract_id,cl_id,con_id,con,cur):
    """ insert sinister informations 
        for a client
    """
 
    psql=f""" insert into sinisters 
                ( sinister_date,
                description,
                opposing_insurer,
                amount,
                extern_id,
                contract_id,
                client_id,
                extern_client_id,
                extern_contract_id
                )
            values {
                sinister.sinister_date,
                sinister.description,
                sinister.opposing_insurer,
                sinister.amount,
                extern_id,
                con_id,
                cl_id,
                id,
                contract_id};"""
    cur.execute(psql)
    print(psql)
    con.commit()


def add_sinister_(sinister,extern_id,id,contract_id,cl_id,con_id,con,cur):
    """ insert sinister informations 
        for a client
    """
 
    psql=f"""insert into sinisters 
                ( sinister_date,
                description,
                opposing_insurer,
                amount,
                extern_id,
                contract_id,
                company_id,
                extern_client_id,
                extern_contract_id
                )
            values {
                sinister.sinister_date,
                sinister.description,
                sinister.opposing_insurer,
                sinister.amount,
                extern_id,
                con_id,
                cl_id,
                id,
                contract_id
                };"""
   
    cur.execute(psql)
    print(psql)
    con.commit()


def update_one_sinister(update_dict,id,sinister_id,con,cur):
    """
    update sinisters table for specified client from database using information from dict
    """
    psql="update sinisters set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{sinister_id}' and extern_client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    print(psql)
    cur.execute(psql)
    con.commit()

    


    
def sinister_to_update(id,sinister_id,con,cur):
    """
    retrieve information from data base for a specified sinister
    """
  
    psql_sinister=f"""select * from sinisters where extern_id='{sinister_id}' and extern_client_id='{id}'"""
    cur.execute(psql_sinister)
    record=cur.fetchall()
    print(record)
    sinister=Sinister(
        id=record[0][1],
        description=record[0][2],
        sinister_date=record[0][4],
        opposing_insurer=record[0][7],
        status=record[0][5],
        amount=record[0][8])
  

    return sinister

def search_sinister_(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    if search_dict!={}:

        psql_base=""" select * from sinisters
        where """

        psql_where=""
        
        for (key,value) in search_dict.items() :
            psql_where= f"""{key}='{value}' and """+psql_where

        psql=psql_base+psql_where[:-4]+";"

        cur.execute(psql)
        record=cur.fetchall()
    else:
        record=None
    columns_names=['id','description','creation_date','status','closing_date','opposing_insurer','amount','client_id']
    return columns_names,record

def search_sinister(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    page_result=5
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key in ['creation_date','closing_date']:

                psql_where= f"""{key} {value} and """+psql_where
            else:
                psql_where= f"""{key}='{value}' and """+psql_where

        psql_base=f""" 
        select extern_id,DESCRIPTION,creation_date,status,closing_date,opposing_insurer,amount,extern_client_id,(select count(*) from sinisters where {psql_where[:-4]}),extern_contract_id from sinisters
        where """
        
       
        offset=0
        
        offset=page_result*(nb_page-1)

        psql_page=f"""ORDER BY id
        OFFSET {offset} ROWS
        FETCH NEXT {page_result} ROWS ONLY"""

        psql=psql_base+psql_where[:-4]+psql_page
        print(psql)
        cur.execute(psql)
        record=cur.fetchall()
        print("record")
        if record:
            count=record[0][8]
        else:
            record=None
            count=None
    else:
        record=None
        count=None
    columns_names=['Description','Date de creation','Statu','date de cloture ','opposing_insurer','amount','client_id','Link']
   
    return count,page_result,columns_names,record
def search_sinister_export(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
   # page_result=5
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key in ['creation_date','closing_date']:

                psql_where= f"""{key} {value} and """+psql_where
            else:
                psql_where= f"""{key}='{value}' and """+psql_where

        psql_base=f""" 
        select extern_id,DESCRIPTION,creation_date,status,closing_date,opposing_insurer,amount,extern_contract_id,(select count(*) from sinisters where {psql_where[:-4]})from sinisters
        where """
        
       
        # offset=0
        
        # offset=page_result*(nb_page-1)

        # psql_page=f"""ORDER BY id
        # OFFSET {offset} ROWS
        # FETCH NEXT {page_result} ROWS ONLY"""

        psql=psql_base+psql_where[:-4]
        print(psql)
        cur.execute(psql)
        record=cur.fetchall()
        
        if record:
            pass
        else:
            record=None
            
    else:
        record=None
       
    
   
    return record

def search_all_sinister(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    record=None
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key in ['creation_date','closing_date']:

                psql_where= f"""{key} {value} and """+psql_where
            else:
                psql_where= f"""{key}='{value}' and """+psql_where

        psql_base=f""" 
        select extern_id,DESCRIPTION,creation_date,status,closing_date,opposing_insurer,amount,extern_client_id,(select count(*) from sinisters where {psql_where[:-4]})from sinisters
        where """
        
        psql=psql_base+psql_where[:-4]
        cur.execute(psql)
        record=cur.fetchall()
        print(record)
    else:
        record=None
       
    
   
    return record
def update_one_modifications(update_dict,id,sinister_id,con,cur):
    """
    update modifications table for specified client from database using information from dict
    """
    psql="update modifications set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where updated_id='{sinister_id}' and updated_by_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)

    con.commit()

def add_modification(modification,con,cur):
    """ insert sinister informations 
        for a client
    """
    psql=f""" insert into modifications
            (
                updated_id,
                updates_values,
                updated_by,
                extern_id
                )
            values {
                modification['updated_id'],
                modification['updates_values'],
                modification['updated_by'],
                modification['extern_id']
                };"""
    cur.execute(psql)
    con.commit()

def count_modification(updated_id,con,cur):
    """ insert sinister informations 
        for a client
    """
    psql=f""" select count(*) from modifications where updated_id='{updated_id}' ;"""
    cur.execute(psql)
    record=cur.fetchone()
    return record[0]