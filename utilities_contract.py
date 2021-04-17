def get_contract_id(extern_id,con,cur):
    """get client id """
    psql=f"""select id from contracts where extern_id='{extern_id}'"""
    cur.execute(psql)
    id=cur.fetchone()[0]
    
    return id
def insert_contract_info_company(contract,company_id,con,cur):
    print('hello')
    psql_contract=f""" insert into contracts
        (extern_id,amount,contract_type,start_date,end_date,company_id)
        values 
        {
            contract.id,
            contract.price,
            contract.contract_type,
            contract.start_date,
            contract.end_date,
            company_id};"""

    cur.execute(psql_contract)
    con.commit()
def insert_contract_info(contract,client_id,con,cur):
    print('hello')
    psql_contract=f""" insert into contracts
        (extern_id,amount,contract_type,start_date,end_date,client_id)
        values 
        {
            contract.id,
            contract.price,
            contract.contract_type,
            contract.start_date,
            contract.end_date,
            client_id};"""

    cur.execute(psql_contract)
    con.commit()

def update_one_contract(update_dict,id,contract_id,con,cur):
    """
    update contract table of a specified contract 
    for a specified client from database using information from dict
    """
    psql="update contracts set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{contract_id}' and client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()


def update_one_contract_(update_dict,id,contract_id,con,cur):
    """
    update contract table of a specified contract 
    for a specified client from database using information from dict
    """
    psql="update contracts set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{contract_id}' and company_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()

def insert_one_contract(contract,client_id,con,cur):
    """ insert contract informations 
        for a client
    """
    psql_contract=f""" insert into contracts
        (extern_id,amount,contract_type,start_date,end_date,client_id)
        values 
        {
            contract.id,
            contract.price,
            contract.contract_type,
            contract.start_date,
            contract.end_date,
            client_id};"""
            
    cur.execute(psql_contract)
    con.commit()


def show_one_contract_info(client_id,contract_id,cur):
    """
    select one contract informations
    """
    psql=f"""select id,creation_date,start_date,end_date,amount,contract_type,status 
        from contracts 
        where client_id='{client_id}'
        and extern_id='{contract_id}'"""
  
    cur.execute(psql)
    record=cur.fetchall()
    contract={}
    if record :
        contract={'id':record[0][0],
            'date de création':record[0][1],
            'date de début effective':record[0][2],
            'date de clôture':record[0][3],
            'prix':record[0][4],
            'type de contrat':record[0][5],
            'statu':record[0][6],
            'link':''}
    
    return contract



def show_one_contract_info_(company_id,contract_id,cur):
    """
    select one contract informations
    """
    psql=f"""select id,creation_date,start_date,end_date,amount,contract_type,status 
        from contracts 
        where company_id='{company_id}'
        and extern_id='{contract_id}'"""
  
    cur.execute(psql)
    record=cur.fetchall()
    contract={}
    if record :
        contract={'id':record[0][0],
            'date de création':record[0][1],
            'date de début effective':record[0][2],
            'date de clôture':record[0][3],
            'prix':record[0][4],
            'type de contrat':record[0][5],
            'statu':record[0][6],
            'link':''}
    
    return contract


def search_contract_pages(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='start_date'or key=='end_date'or key=='creation_date':
                
                psql_where= f""" con.{key} {value} and """+psql_where
            elif key in ['contract_type','contract_reference','status']:

                psql_where= f""" con.{key}='{value}' and """+psql_where
            elif key in ['con.extrn_id']:

                psql_where= f""" {key}='{value}' and """+psql_where            
            else:
                psql_where= f""" cl.{key}='{value}' and """+psql_where
                
        psql_base=f""" select distinct  name,last_name,email,con.creation_date,start_date,end_date,con.extern_id,cl.extern_id,
        (select count(distinct con.id) 
        from clients cl
        left join contracts con
        on cl.id=con.client_id
        where {psql_where[:-4]}) as nb
        from clients cl
        left join contracts con
        on cl.id=con.client_id
        where """

        offset=0
        page_result=5
        record=None
        offset=offset+page_result*(nb_page-1)
    
        psql_page=f"""ORDER BY cl.extern_id
            OFFSET {offset} ROWS
            FETCH NEXT {page_result} ROWS ONLY"""
        psql=psql_base+psql_where[:-4]+"group by name,last_name,cl.email,con.creation_date,start_date,end_date,con.extern_id,cl.extern_id "+psql_page
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
    columns_names=['Prénom','Nom','email','date de creation','date de debut','date de cloture','référence contract','Link']
    
    return count,page_result,columns_names,record
def search_contract_pages_export(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='start_date'or key=='end_date'or key=='creation_date':
                
                psql_where= f""" con.{key} {value} and """+psql_where
            elif key in ['contract_type','contract_reference','status']:

                psql_where= f""" con.{key}='{value}' and """+psql_where
            elif key in ['con.extern_id']:

                psql_where= f""" {key}='{value}' and """+psql_where            
            else:
                psql_where= f""" cl.{key}='{value}' and """+psql_where
                
        psql_base=f""" select distinct  name,last_name,email,con.creation_date,start_date,end_date,con.extern_id,cl.extern_id,
        (select count(distinct con.id) 
        from clients cl
        left join contracts con
        on cl.id=con.client_id
        where {psql_where[:-4]}) as nb
        from clients cl
        left join contracts con
        on cl.id=con.client_id
        where """

        offset=0
        page_result=5
        record=None
        offset=offset+page_result*(nb_page-1)
    
        # psql_page=f"""ORDER BY cl.id
        #     OFFSET {offset} ROWS
        #     FETCH NEXT {page_result} ROWS ONLY"""
        psql=psql_base+psql_where[:-4]+"group by name,last_name,cl.email,con.creation_date,start_date,end_date,con.extern_id,cl.extern_id "
        cur.execute(psql)
        record=cur.fetchall()
        
        if record :
           pass
        else:
            record=None
            
    else:
        record=None
       
    return record