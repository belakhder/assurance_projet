def insert_address_info_company(address,company_id,extern_company_id,con,cur):
    """insert address data into the database 
    from objects modeling  address
    """
    psql_address=f""" insert into address 
        (extern_id,line1,line2,city,postal_code,state,country,company_id,extern_client_id)
        values 
        {
            address.id,
            address.line1,
            address.line2,
            address.city,
            address.postal_code,
            address.state,
            address.country,
            company_id,
            extern_company_id,};"""
    psql=psql_address
    cur.execute(psql)
    print(psql)
    con.commit()

def update_one_address(update_dict,id,id_address,con,cur):
    """
    update address table for specified client from database using informations from dict
    """
    psql="update address set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{id_address}' and extern_client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()

def insert_address_info(address,client_id,extern_client_id,con,cur):
    """insert address data into the database 
    from objects modeling  address
    """
    psql_address=f""" insert into address 
        (extern_id,line1,line2,city,postal_code,state,country,client_id,extern_client_id)
        values 
        {
            address.id,
            address.line1,
            address.line2,
            address.city,
            address.postal_code,
            address.state,
            address.country,
            client_id,
            extern_client_id,};"""
    psql=psql_address
    cur.execute(psql)
    con.commit()

def update_one_address(update_dict,id,id_address,con,cur):
    """
    update address table for specified client from database using informations from dict
    """
    psql="update address set "
    psql_update=""
    for (key,value) in update_dict.items():
        psql_update=f"{key}='{value}',"+psql_update

    condition=f" where extern_id='{id_address}' and extern_client_id='{id}';"
    psql=psql+psql_update[:-1]+condition
    cur.execute(psql)
    con.commit()

def address_to_update(id,con,cur):
    """
    retrieve information from data base for a specified client
    """

    psql=f"""select line1,line2,city,state,postal_code,country from address where extern_client_id='{id}'"""
    cur.execute(psql)
    record=cur.fetchall()
   
    address={'line1':record[0][0],
        'line2':record[0][1],
        'city':record[0][2],
        'state':record[0][3],
        'postal_code':record[0][4],
        'country':record[0][5]}
    return address