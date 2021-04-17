

from utilities import postgres_connetion,close_postgres_connection
import uuid
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def create_indemnity(sinister,extern_id,cl_id,con_id,id,contract_id,con,cur):
    """ insert indemnities informations 
    retrieved from sinister object and id client
    """
    print(sinister.id,sinister.amount)
    psql_indemnity=f""" insert into indemnities
    (sinister_id,amount,extern_id,client_id,contract_id,extern_client_id,extern_contract_id)
    values 
    {
        sinister.id,
        sinister.amount,
        extern_id,
        cl_id,
        con_id,
        id,
        contract_id};"""
    print(psql_indemnity)
    cur.execute(psql_indemnity)
    con.commit()


def create_indemnity_(sinister,extern_id,cl_id,con_id,id,contract_id,con,cur):
    """ insert indemnities informations 
    retrieved from sinister object and id client
    """
    print(sinister.id,sinister.amount)
    psql_indemnity=f""" insert into indemnities
    (sinister_id,amount,extern_id,company_id,contract_id,extern_client_id,extern_contract_id)
    values 
    {
        sinister.id,
        sinister.amount,
        extern_id,
        cl_id,
        con_id,
        id,
        contract_id};"""
    print(psql_indemnity)
    cur.execute(psql_indemnity)
    con.commit()

def update_one_indemnity(update_dict,id,indemnity_id,con,cur):
    """
    update indemnity table for specified client from database using information from dict
    """
    psql="update indemnities set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{indemnity_id}' and extern_client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    print(psql)
    cur.execute(psql)
    con.commit()


def check_indemnity_status(id,indemnity_id,con,cur):
    """
    Check status indemnities if it is Made or not
    """
    check=False
    psql_sinister=f"""select refund_status from indemnities where extern_id='{indemnity_id}' and extern_client_id='{id}'"""
    cur.execute(psql_sinister)
    record=cur.fetchall()
    
    if record[0][0]=='Effectué':
        check=True

    return check

def search_indemnity(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    page_result=0
    if search_dict!={}:

        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='creation_date':
                psql_where= f"""indem.{key} {value} and """+psql_where
            else:
                psql_where= f"""indem.{key}='{value}' and """+psql_where
        
        psql_base=f""" select indem.extern_id,description,indem.amount,refund_status,indem.extern_client_id,indem.creation_date,(select count(*) 
        from indemnities indem
        left join sinisters on sinisters.extern_id=indem.sinister_id
        where {psql_where[:-4]}),indem.extern_contract_id
        from indemnities indem
        left join sinisters on sinisters.extern_id=indem.sinister_id
        
        where """
        offset=0
        page_result=5
        offset=page_result*(nb_page-1)
        psql_page=f"""ORDER BY indem.id
        OFFSET {offset} ROWS
        FETCH NEXT {page_result} ROWS ONLY"""
        
        psql=psql_base+psql_where[:-4]+psql_page
        
        cur.execute(psql)
        print(psql)
        record=cur.fetchall()
        
        if record:
            count=record[0][6]
        else:
            record=None
            count=None
    else:
        record=None
        count=None
    columns_names=['description','montant','status','date de creation','réference client','Link']

    return count,page_result,columns_names,record
def search_indemnity_export(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    #page_result=0
    if search_dict!={}:

        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='creation_date':
                psql_where= f"""indem.{key} {value} and """+psql_where
            else:
                psql_where= f"""indem.{key}='{value}' and """+psql_where
        
        psql_base=f""" select indem.extern_id,description,indem.amount,refund_status,indem.extern_client_id,indem.creation_date,(select count(*) 
        from indemnities indem
        left join sinisters on sinisters.extern_id=indem.sinister_id
        where {psql_where[:-4]})
        from indemnities indem
        left join sinisters on sinisters.extern_id=indem.sinister_id
        
        where """
        # offset=0
        #page_result=5
        #offset=page_result*(nb_page-1)
        # psql_page=f"""ORDER BY indem.id
        # OFFSET {offset} ROWS
        # FETCH NEXT {page_result} ROWS ONLY"""
        
        psql=psql_base+psql_where[:-4]
        
        cur.execute(psql)
        
        record=cur.fetchall()
        
        if record:
            pass
        else:
            record=None
     
    else:
        record=None
        
    

    return record


def delete_one_indemnity(condition,value,con,cur):
    """ Delete specified indemnity"""

    psql=f"""DELETE FROM indemnities WHERE {condition} ='{value}';"""

    cur.execute(psql)
    con.commit()

def indemnity_to_update(id,con,cur):
    """
    retrieve information from data base for a specified indemnity
    """

    psql=f"""select amount from indemnities where extern_id='{id}'"""
    cur.execute(psql)
    record=cur.fetchall()
    
    indemnity={'amount':record[0][0]}

    return indemnity