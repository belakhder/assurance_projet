def get_company_id(company_email,con,cur):
    """get company id """
    psql=f"""select id from companies where company_email='{company_email}'"""
    cur.execute(psql)
    id=cur.fetchone()[0]
    print(id)
    return id

def get_company_by_extern_id(extern_id,con,cur):
    """get company id """
    psql=f"""select id from companies where extern_id='{extern_id}'"""
    cur.execute(psql)
    id=cur.fetchone()[0]
    print(id)
    return id
def insert_company_info(company,con,cur):
    """insert company data into the database 
    from objects modeling company info
    """
    
    psql_company=f""" insert into companies 
        (extern_id,company_name,company_email,company_tel,company_registration_nb,company_type)
        values {
            company.id,
            company.company_name,
            company.company_email,
            company.company_tel,
            company.company_registration_nb,
            company.company_type
            };"""
    cur.execute(psql_company)
    con.commit()
# def insert_client_info(keys,values,client,contract,con,cur):
#     """insert customer data into the database 
#     from objects modeling customer contract address
#     """

#     psql_client=f""" insert into clients 
#         (extern_id,name,last_name,email,tel,client_type)
#         values {
#             client.id,
#             client.name,
#             client.last_name,
#             client.email,
#             client.tel,
#             client.client_type
#             };"""
#     psql_address=f""" insert into address 
#         (extern_id,line1,line2,city,postal_code,state,country,client_id)
#         values 
#         {
#             client.address.id,
#             client.address.line1,
#             client.address.line2,
#             client.address.city,
#             client.address.postal_code,
#             client.address.state,
#             client.address.country,
#             client.id};"""
#     psql_contract=f""" insert into contracts
#         (extern_id,price,contract_type,start_date,end_date,client_id)
#         values 
#         {
#             contract.id,
#             contract.price,
#             contract.contract_type,
#             contract.start_date,
#             contract.end_date,
#             client.id};"""
#     if keys!='':
#         psql_payment=f""" insert into payments ({keys}) values {values};"""
#     else:
#         psql_payment=""

#     psql=psql_client
#     print(psql)
#     cur.execute(psql)
    
#     con.commit()

def search_client(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    print('jhx<qshcbw<xchbw<x')
    if search_dict!={}:

        psql_base=""" select distinct cl.id, name,last_name,email,tel 
        from clients cl
        left join contracts con
        on cl.id=con.client_id
        where """

        psql_where=""
        
        for (key,value) in search_dict.items() :
            psql_where= f"""{key}='{value}' and """+psql_where

        psql=psql_base+psql_where[:-4]+";"
        cur.execute(psql)
        record=cur.fetchall()

    else:
        record=None
    columns_names=['reference','name','last_name','email','tel','Link']
    
    return columns_names,record


   

def search_fiche_client(id,contract_id,cur):
    """
        get search criteria from a dict create sql statement 
        return filtred results
    """
    
    psql=f""" SELECT Distinct cl.extern_id,company_name,company_name,company_email,company_tel
        ,array_agg(con.extern_id order by con.id ),array_agg(con.creation_date order by con.id)
        ,array_agg(start_date order by con.id),array_agg(end_date order by con.id),array_agg(con.amount order by con.id)
        ,array_agg(contract_type order by con.id),array_agg(con.status order by con.id),
        ad.extern_id,line1,line2,city,postal_code,state,country
        ,(select array_agg(extern_id order by extern_id) from sinisters where extern_contract_id ='{contract_id}')
        ,(select array_agg(description order by extern_id) from sinisters where extern_contract_id ='{contract_id}' ),
        (select array_agg(sinister_date order by extern_id) from sinisters where extern_contract_id ='{contract_id}'),
        (select array_agg(status order by extern_id) from sinisters where extern_contract_id ='{contract_id}'),
        (select array_agg(closing_date order by extern_id) from sinisters where extern_contract_id ='{contract_id}'),
        (select array_agg(opposing_insurer order by extern_id) from sinisters where extern_contract_id ='{contract_id}'),
        (select array_agg(amount order by extern_id) from sinisters where extern_contract_id ='{contract_id}'),
        (select array_agg(extern_id order by extern_id) from indemnities where extern_contract_id ='{contract_id}'),
        (select array_agg(sinister_id order by extern_id) from indemnities where extern_contract_id ='{contract_id}'),
        (select array_agg(amount order by extern_id) from indemnities where extern_contract_id ='{contract_id}'),
        (select array_agg(refund_status order by extern_id) from indemnities where extern_contract_id ='{contract_id}'),
        (select array_agg(creation_date order by extern_id) from indemnities where extern_contract_id ='{contract_id}'),
        (SELECT sum(amount) from instalments where due_date<now() and status !='Payé' group by extern_client_id,extern_contract_id HAVING extern_client_id='{id}' and extern_contract_id ='{contract_id}') as impayé,
        (SELECT array_agg(extern_id) from instalments where due_date-date(now()) < -1   group by extern_client_id,extern_contract_id,status HAVING extern_client_id='{id}' and extern_contract_id ='{contract_id}' and status !='Payé') as relance,
        (SELECT count(extern_id) from instalments  group by extern_client_id,extern_contract_id HAVING extern_client_id='{id}' and extern_contract_id ='{contract_id}' ) as nb
        from companies cl
        left join address ad on cl.id= ad.company_id
        left join contracts con on cl.id=con.company_id
        left join sinisters sin on cl.id=sin.company_id
        left join indemnities indem on cl.id=indem.company_id
        
        where cl.extern_id='{id}'
        
        group by cl.id,company_name,company_email,company_tel,con.client_id,ad.id,country
        ; """
        
    contracts=[]
    client_info={}
    address_info={}
    contracts=[]
    sinisters=[]
    indemnities=[]
    cur.execute(psql)
    record=cur.fetchall()
 
    total_indemnities=0
    unpaid=0
    relance=[]
   
    if record:
        client_info={
            'id':record[0][0],
            'Nom De Société':record[0][1],
            'email':record[0][3],
            'tel':record[0][4]}
        ids=[]
        
        for i in range(len(record[0][5])):
            if record[0][5][i] not in ids :
                ids.append(record[0][5][i])            
                contracts.append({'id':record[0][5][i],
                    'date de création':record[0][6][i],
                    'date de début effective':record[0][7][i],
                    'date de clôture':record[0][8][i],
                    'prix':record[0][9][i],
                    'type de contrat':record[0][10][i],
                    'statu':record[0][11][i],
                    'link':''})
        
        address_info={
            'id':record[0][12],
            'ligne1':record[0][13],
            'ligne2':record[0][14],
            'ville':record[0][15],
            'code postal':record[0][16],
            'etat':record[0][17],
            'pays':record[0][18]
            }
        ids=[]
        
        if record[0][19]:
            for i in range(len(record[0][19])):
                if record[0][19][i] not in ids :
                    ids.append(record[0][19][i])
                    sinisters.append({'id':record[0][19][i],
                        'Description':record[0][20][i],
                        'Date de sinistre':record[0][21][i],
                        'Statu':record[0][22][i],
                        'Date de clôture':record[0][23][i],
                        'Assureur adversaire':record[0][25][i],
                        'Montant':record[0][24][i],
                        'Link':''})
        ids=[]
        indem=[]

        if record[0][26]:
            for i in range(len(record[0][26])):
                if record[0][26][i] not in ids :
                    ids.append(record[0][26][i])
                    if (isinstance(record[0][28][i],int) or isinstance(record[0][28][i],float)) and record[0][29][i]=='Not Made' :
                        indem.append(record[0][28][i])
                        total_indemnities=total_indemnities+record[0][28][i]
                    indemnities.append({'id':record[0][26][i],
                        'Sinistre':record[0][27][i],
                        'Montant':record[0][28][i],
                        'Statu':record[0][29][i],
                        'Date de création':record[0][30][i],
                        'Link':''
                        })

        if record[0][31] !=None:
            unpaid=round(record[0][31],2)
            print(unpaid)
        else:
            unpaid=0
        relance=record[0][32]
        nb=record[0][33]
    return [client_info,contracts,address_info,sinisters,indemnities,total_indemnities,record,unpaid,relance,nb]


def update_client_info(update_dict,id,con,cur):
    """
    update client table from database using information from dict
    """
    
    psql="update clients set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()


def get_all_company(nb_page,cur):
    
    """
        get all companies from database diplayed on pages
    """
    
    page_result=15
    offset=0
    offset=offset+page_result*(nb_page-1)
   
    psql_base=""" select distinct  companies.extern_id,company_name,company_email,company_tel,array_agg(contracts.extern_id),companies.id,array_agg(contracts.extern_id),(
    select count(*)
    from companies) as tot,company_type
    from companies
    left join contracts
    on companies.id=contracts.company_id
    GROUP by companies.id,company_name,company_email,company_tel 
    """
  
    psql_page=f"""ORDER BY companies.extern_id desc
    OFFSET {offset} ROWS
    FETCH NEXT {page_result} ROWS ONLY"""
    psql=psql_base
    cur.execute(psql)
    record=cur.fetchall()
    print(len(record))
    columns_names=['Reference client','Société','Email','Tel','Company type','Link']
    if record:
        count=record[0][7]
    else :
        record=None
        count=0
    
    return count,page_result,columns_names,record

def search_client_pages(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    print('heloo5454654')
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='start_date'or key=='end_date':
                
                psql_where= f""" con.{key} {value} and """+psql_where
            elif key in ['contract_type','contract_reference','status']:

                psql_where= f""" con.{key}='{value}' and """+psql_where
            elif key in ['con.id']:

                psql_where= f""" {key}='{value}' and """+psql_where            
            else:
                psql_where= f""" cl.{key}='{value}' and """+psql_where
                
        psql_base=f""" select distinct cl.id, name,last_name,email,tel,array_agg(con.id),
        (select count(distinct cl.id) 
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
    
        psql_page=f"""ORDER BY cl.id
            OFFSET {offset} ROWS
            FETCH NEXT {page_result} ROWS ONLY"""
        psql=psql_base+psql_where[:-4]+"group by cl.id,name,last_name,email,tel "+psql_page
        cur.execute(psql)
        record=cur.fetchall()
        print(psql)
        if record :
            count=record[0][6]
        else:
            record=None
            count=None
    else:
        record=None
        count=None
    columns_names=['Réference client','Prénom','Nom','Email','Tel','Link']
    print('1010101010101010')
    print(psql)
    return count,page_result,columns_names,record



def search_company_pages_export(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    
    if search_dict!={}:
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='start_date'or key=='end_date':
                
                psql_where= f""" con.{key} {value} and """+psql_where
            elif key in ['contract_type','contract_reference','status']:

                psql_where= f""" con.{key}='{value}' and """+psql_where
            elif key in ['con.extern_id']:

                psql_where= f""" {key}='{value}' and """+psql_where            
            else:
                psql_where= f""" cl.{key}='{value}' and """+psql_where
                
        psql_base=f""" select distinct cl.id, company_name,company_email,company_tel,array_agg(con.id),
        (select count(distinct cl.id) 
        from companies cl
        left join contracts con
        on cl.id=con.company_id
        where {psql_where[:-4]}) as nb
        from companies cl
        left join contracts con
        on cl.id=con.company_id
        where """

        offset=0
        page_result=5
        record=None
        offset=offset+page_result*(nb_page-1)
    
        # psql_page=f"""ORDER BY cl.id
        #     OFFSET {offset} ROWS
        #     FETCH NEXT {page_result} ROWS ONLY"""
        psql=psql_base+psql_where[:-4]+"group by cl.id,company_name,company_email,company_tel "
        cur.execute(psql)
        record=cur.fetchall()
        print(psql)
        if record :
            pass
        else:
            record=None
    else:
        record=None
    return record
def delete_one_client(id,con,cur):
    """
    delete one client 
    """
    psql_clients="DELETE FROM clients"

    condition=f" where id='{id}';"
    condition_client=f" where client_id='{id}';"
    psql_contract="DELETE FROM contracts"
    psql_sinisters="DELETE FROM sinisters"
    psql_indemnities="DELETE FROM indemnities"

    psql=(psql_clients+condition
        +psql_contract+condition_client
        +psql_sinisters+condition_client
        +psql_indemnities+condition_client
        )
   
    cur.execute(psql)
    con.commit()






def company_to_update(id,con,cur):
    """
    retrieve information from data base for a specified company
    """

    psql=f"""select company_name,company_email,company_tel from companies where extern_id='{id}'"""
    cur.execute(psql)
    record=cur.fetchall()
    client={'company_name':record[0][0],'company_emai':record[0][1],'company_tel':record[0][2]}

    return client


def update_company_info(update_dict,id,con,cur):
    """
    update client table from database using information from dict
    """
    psql="update companies set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()

def search_company_pages(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    if search_dict!={}:
        
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='start_date'or key=='end_date':
                
                psql_where= f""" con.{key} {value} and """+psql_where
            elif key in ['contract_type','contract_reference','status']:

                psql_where= f""" con.{key}='{value}' and """+psql_where
            elif key in ['con.extern_id']:
                print(key)
                
                psql_where= f""" {key}='{value}' and """+psql_where            
                
            else:
                print('dnbqdb,nsdfsdns,nds,nds,nd')
                psql_where= f""" cl.{key}='{value}' and """+psql_where
        
        psql_base=f""" select distinct cl.extern_id, company_name,company_email,company_tel,array_agg(con.extern_id),
        (select count(distinct cl.id) 
        from companies cl
        left join contracts con
        on cl.id=con.company_id
        where {psql_where[:-4]}) as nb
        from companies cl
        left join contracts con
        on cl.id=con.company_id
        where """

        offset=0
        page_result=5
        record=None
        offset=offset+page_result*(nb_page-1)
    
        psql_page=f"""ORDER BY cl.extern_id
            OFFSET {offset} ROWS
            FETCH NEXT {page_result} ROWS ONLY"""
        psql=psql_base+psql_where[:-4]+"group by cl.extern_id,company_name,company_email,company_tel "+psql_page
        print(psql)
        cur.execute(psql)
        record=cur.fetchall()
        
        if record :
            count=record[0][5]
        else:
            record=None
            count=None
    else:
        record=None
        count=None
    columns_names=['Réference client','Société','Email','Tel','Link']
  
    return count,page_result,columns_names,record
