

def insert_one_client_payments (payments,id,contract_id,con,cur):
    """ 
        insert payment informations 
        for a client
    """
    psql=""
    for inst in payments:
    
        
        psql=psql+f""" insert into payments
                (   
                    due_date,
                    amount,
                    remaining_amount,
                    client_id,
                    contract_id)
                values{
                    inst.due_date,
                    inst.amount,
                    inst.amount,
                    id,
                    contract_id};"""
    print(psql)
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





def show_client_payments(client_id,contract_id,cur):
    """
        get all payments client for one contrcat from database diplayed on pages
    """

    psql_base=f"""select inst.extern_id,inst.due_date,inst.amount,remaining_amount,
    (select sum(remaining_amount) from payments where extern_client_id='{client_id}'  and extern_contract_id='{contract_id}') as somme,(
    select count(*)
    from payments) as tot,array_agg(pay.payment_date) payment_dates
    from instalments inst
    left join payments pay
    on inst.extern_id=pay.inst_id
    where inst.extern_client_id='{client_id}' and inst.extern_contract_id='{contract_id}'
    GROUP by inst_id,inst.client_id,due_date,inst.contract_id,tot,inst.amount,inst.remaining_amount,inst.id
    order by inst.id
    """
    
    psql_page=""
    psql=psql_base+psql_page
    cur.execute(psql)
    
    record=cur.fetchall()
   
    cur.execute("SELECT Column_name  FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'payments'")
    col=cur.fetchall()
    
    columns=[col[0][0],col[1][0],col[2][0],col[3][0],col[4][0],col[5][0],col[6][0]]

    columns_names=["date d'échéance","Date Du Dernier Paiement","restant due","montant",'mode de paiement','status','reference client','reference contract']

    return columns,columns_names,record

def update_payment(update_dict,id,inst_id,con,cur):
    """
    update payments table for specified client from database using information from dict
    """
    psql="update payments set "
    psql_update=""
    psql_satus=""

    for (key,value) in update_dict.items():
        if key=='remaining_amount':
            psql_satus=f"status=(case when {key}-{value}=0 then 'payé' else status end ) "
            psql_update=f"{key}={key}-{value},"+psql_update+psql_satus
        else:
            psql_update=f"{key}='{value}',"+psql_update
        
    condition=f"  where id='{inst_id}' and client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()


def add_payment(keys,values,con,cur):
    """ insert payments informations 
        for a client
    """
    
    psql=f""" insert into payments ({keys}) values {values};"""
    print('psql')
    print(psql)
    print(psql)
    cur.execute(psql)
    con.commit()

def search_payment(search_dict,nb_page,cur):
    
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    page_result=5
    if search_dict!={}:

        psql_where=""
        
        for (key,value) in search_dict.items() :

            if key=='payment_date':
                
                psql_where= f""" payments.{key} {value} and """+psql_where
            else:
                psql_where= f""" payments.{key}='{value}' and """+psql_where
        
        psql_base=f""" select * ,(select count(*) 
        from payments
        where {psql_where[:-4]})from payments
        
        where """
        offset=0
       
        offset=page_result*(nb_page-1)
        psql_page=f"""ORDER BY payments.id
        OFFSET {offset} ROWS
        FETCH NEXT {page_result} ROWS ONLY"""
        
        psql=psql_base+psql_where[:-4]+psql_page
      
        cur.execute(psql)
        record=cur.fetchall()
        
        if record:
            print(record)
            count=record[0][16]
        else:
            record=None
            count=None
    else:
        record=None
        count=None

    columns_names=["date de paiement","Montant payé","mode de paiment","référence client","Référence Du Contract",'Link']
    
    return count,page_result,columns_names,record

def search_all_payment(search_dict,cur):
    
    """
        get search criteria from a dict create sql statement return
        filtred results
    """
    record=None
    if search_dict!={}:

        psql_where=""
        
        for (key,value) in search_dict.items() :

            if key=='payment_date':
                
                psql_where= f""" payments.{key} {value} and """+psql_where
            else:
                psql_where= f""" payments.{key}='{value}' and """+psql_where
        
        psql_base=f""" select * ,(select count(*) 
        from payments
        where {psql_where[:-4]})from payments
        
        where """

        
        psql=psql_base+psql_where[:-4]
        cur.execute(psql)
        record=cur.fetchall()

    else:
        record=None

    return record