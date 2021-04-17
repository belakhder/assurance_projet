

def insert_one_client_instalments (instalments,client_id,ctr_id,id,contract_id,con,cur):
    """ 
        insert instalment informations 
        for a client
    """
    psql=""
    for inst,extern_id in instalments:
    
        
        psql=psql+f""" insert into instalments
                (   
                    due_date,
                    amount,
                    remaining_amount,
                    extern_id,
                    client_id,
                    contract_id,
                    extern_client_id,
                    extern_contract_id)
                values{
                    inst.due_date,
                    inst.amount,
                    inst.amount,
                    extern_id,
                    client_id,
                    ctr_id,
                    id,
                    contract_id
                    };"""

    cur.execute(psql)
    con.commit()

# def update_one_indtalment(update_dict,id,inst_id,con,cur):
#     """
#     update bills table for specified client from database using information from dict
#     """
#     psql="update bills set "
#     psql_update=""
#     for (key,value) in update_dict.items():
#         psql_update=f"{key}='{value}',"+psql_update

#     condition=f" where id='{inst_id}' and client_id='{id}';"
#     psql=psql+psql_update[:-1]+condition
#     cur.execute(psql)
#     con.commit()





def show_client_instalments(client_id,contract_id,cur):
    """
        get all instalments client for one contrcat from database diplayed on pages
    """

    psql_base=f"""select inst.extern_id,due_date,inst.amount,remaining_amount,
    (select sum(remaining_amount) from instalments where extern_client_id='{client_id}'  and extern_contract_id='{contract_id}') as somme,(
    select count(*)
    from instalments) as tot,array_agg(pay.payment_date) payment_dates,inst.client_id,inst.contract_id,
    (select name from clients where extern_id='{client_id}'),
    (select last_name from clients where extern_id='{client_id}')
    from instalments inst
    left join payments pay
    on inst.extern_id=pay.inst_id
    where inst.extern_client_id='{client_id}' and inst.extern_contract_id='{contract_id}'
    GROUP by inst_id,inst.client_id,due_date,inst.contract_id,somme,tot,inst.amount,inst.remaining_amount,inst.id
    order by inst.id
    """
    
    psql_page=""
    psql=psql_base+psql_page
    cur.execute(psql)
    
    record=cur.fetchall()
   
    cur.execute("SELECT Column_name  FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'instalments'")
    col=cur.fetchall()
    
    columns=[col[0][0],col[1][0],col[2][0],col[3][0],col[4][0],col[5][0],col[6][0]]

    columns_names=["date d'echeance","Date Du Dernier Paiement","restant due","montant",'mode de paiement','status','reference client','reference contract']
  
    return columns,columns_names,record

def update_instalment(update_dict,id,inst_id,con,cur):
    """
    update instalments table for specified client from database using information from dict
    """
    psql="update instalments set "
    psql_update=""
    psql_satus=""
    
    
    for (key,value) in update_dict.items():
        if key=='remaining_amount':
            
            psql_satus=f"status=(case when {key}-{value}=0 then 'Payé' when {key}-{value} > 0 then 'Partiellement Payé' else status end ) "
            psql_update=f"{key}=round(CAST(float8 ({key}-{value}) as numeric),2),"+psql_update+psql_satus
        else:
            psql_update=f"{key}='{value}',"+psql_update
        
    condition=f"  where extern_id='{inst_id}' and extern_client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
 
    cur.execute(psql)
    con.commit()

def add_payment(values,keys,con,cur):
    """ insert payments informations 
        for a client
    """
    print('heelllll')
    psql=f""" insert into payments ({keys}) values {values};"""
    print(psql)
    cur.execute(psql)
    
    con.commit()

def search_instalment(search_dict,nb_page,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    page_result=5
    if search_dict!={}:
        
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='due_date':
                psql_where= f""" instalments.{key} {value} and """+psql_where
            else:
                psql_where= f""" instalments.{key}='{value}' and """+psql_where
        
        psql_base=f""" select extern_id,due_date,amount,status,remaining_amount,extern_client_id,extern_contract_id ,(select count(*) 
        from instalments
        where {psql_where[:-4]})from instalments
        
        where """
        offset=0
        page_result=5
        offset=page_result*(nb_page-1)
        psql_page=f"""ORDER BY instalments.extern_id
        OFFSET {offset} ROWS
        FETCH NEXT {page_result} ROWS ONLY"""
        
        psql=psql_base+psql_where[:-4]+psql_page
        
        cur.execute(psql)
        
        record=cur.fetchall()
       
        if record:
            count=record[0][7]
        else:
            record=None
            count=None
    else:
        record=None
        count=None

    columns_names=["date d'échéance","Montant","statu","Restant De L'échéance","référence client","Référence Du Contract",'Link']
    
    return count,page_result,columns_names,record

def search_all_instalment(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
  
    if search_dict!={}:
        
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='due_date':
                psql_where= f""" instalments.{key} {value} and """+psql_where
            else:
                psql_where= f""" instalments.{key}='{value}' and """+psql_where
        
        psql_base=f""" select extern_id,due_date,amount,status,remaining_amount,extern_client_id,extern_contract_id ,(select count(*) 
        from instalments
        where {psql_where[:-4]})from instalments
        
        where """

        
        psql=psql_base+psql_where[:-4]

  
        cur.execute(psql)
        
        record=cur.fetchall()

    else:
        record=None
    columns = ['id',"date d'echeance",'montant','statu','restant due','reference client','nombre de résultat']
    return record,columns

def search_one_instalment(search_dict,cur):
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
  
    if search_dict!={}:
        
        psql_where=""
        
        for (key,value) in search_dict.items() :
            if key=='due_date':
                psql_where= f""" instalments.{key} {value} and """+psql_where
            else:
                psql_where= f""" instalments.{key}='{value}' and """+psql_where
        
        psql_base=f""" select extern_id,due_date,amount,status,remaining_amount,extern_client_id,extern_contract_id ,(select count(*) 
        from instalments
        where {psql_where[:-4]})from instalments
        
        where """

        
        psql=psql_base+psql_where[:-4]

     
        cur.execute(psql)
        
        record=cur.fetchone()

    else:
        record=None
    columns = ['id',"date d'echeance",'montant','statu','restant due','reference client','nombre de résultat']
    
    return record,columns

def insert_one_company_instalments (instalments,company_id,ctr_id,id,contract_id,con,cur):
    """ 
        insert instalment informations 
        for a client
    """
    psql=""
    for inst,extern_id in instalments:
    
        
        psql=psql+f""" insert into instalments
                (   
                    due_date,
                    amount,
                    remaining_amount,
                    extern_id,
                    company_id,
                    contract_id,
                    extern_client_id,
                    extern_contract_id)
                values{
                    inst.due_date,
                    inst.amount,
                    inst.amount,
                    extern_id,
                    company_id,
                    ctr_id,
                    id,
                    contract_id
                    };"""

    cur.execute(psql)
    con.commit()


def show_company_instalments(client_id,contract_id,cur):
    """
        get all instalments client for one contrcat from database diplayed on pages
    """

    psql_base=f"""select inst.extern_id,due_date,inst.amount,remaining_amount,
    (select sum(remaining_amount) from instalments where extern_client_id='{client_id}'  and extern_contract_id='{contract_id}') as somme,(
    select count(*)
    from instalments) as tot,array_agg(pay.payment_date) payment_dates,inst.client_id,inst.contract_id,
    (select name from companies where extern_id='{client_id}'),
    (select last_name from companies where extern_id='{client_id}')
    from instalments inst
    left join payments pay
    on inst.extern_id=pay.inst_id
    where inst.extern_client_id='{client_id}' and inst.extern_contract_id='{contract_id}'
    GROUP by inst_id,inst.client_id,due_date,inst.contract_id,somme,tot,inst.amount,inst.remaining_amount,inst.id
    order by inst.id
    """
    
    psql_page=""
    psql=psql_base+psql_page
    cur.execute(psql)
    
    record=cur.fetchall()
   
    cur.execute("SELECT Column_name  FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'instalments'")
    col=cur.fetchall()
    
    columns=[col[0][0],col[1][0],col[2][0],col[3][0],col[4][0],col[5][0],col[6][0]]

    columns_names=["date d'echeance","Date Du Dernier Paiement","restant due","montant",'mode de paiement','status','reference client','reference contract']
  
    return columns,columns_names,record