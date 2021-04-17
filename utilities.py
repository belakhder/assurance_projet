import psycopg2
import re
from config import *
import datetime
import calendar
import csv
import datetime
def postgres_connetion(host,db_name,db_user,db_password):
    try:
        con = psycopg2.connect(f" host={host} dbname={db_name} user={db_user} password={db_password}")
    except Exception as error:
        con=None
        print(f"{error}")
    return con



def close_postgres_connection(cur,con):
    if(con != None):
        cur.close()
        con.close()


def current_user(id):
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f""" select id,user_type,last_name,name,(select count(*) from users where user_type='Manager') as manager
    ,(select count(*) from users where user_type='Conseiller client') as cc
    from users where id='{id}'""")
    cur.execute(psql)
    record=cur.fetchone()
    return record

def to_csv(file_name,columns,data):
    with open(f'csv_file/{file_name}','w',newline='') as f:
        thewriter=csv.writer(f)

        thewriter.writerow(columns)
        
        for row in data:
            print(row)
            thewriter.writerow(row)
    with open(f'csv_file/{file_name}','r') as f:
        csv_file=f.read()
    return csv_file


def time_number():
    """
    change the date to a  numeric string
    """
    date=datetime.datetime.now()
    time="".join(str(date)[-15:-7].split(":"))
    time="".join(str(date)[0:-16].split("-"))+time[1:]
    return time

def loads_settings():
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f""" select step,max_inst
        from settings where id= '1'""")
    cur.execute(psql)
    record=cur.fetchone()

    return record

def money_contract(start,end):

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f"""select sum(amount),
    sum(amount)/(select sum(amount) from contracts where creation_date between '{start}' and  '{end}' ),
    STATUS 
    from contracts 
    where creation_date 
    between '{start}' and  '{end}' group by status; """)
    cur.execute(psql)
    record=cur.fetchall()
    
    return record

def money_instalment(start,end):

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f"""select sum(amount),
    sum(amount)/(select sum(amount) from instalments where due_date between '{start}' and  '{end}' ),
    STATUS 
    from instalments 
    where due_date 
    between '{start}' and  '{end}' group by status; """)
    cur.execute(psql)
    record=cur.fetchall()
    print(psql)
    return record

def money_payment(start,end):

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f"""select sum(payment_amount),
    sum(payment_amount)/(select sum(payment_amount) from payments where payment_date between '{start}' and  '{end}' ),
    payment_mode
    from payments 
    where payment_date
    between '{start}' and  '{end}' group by payment_mode; """)
    cur.execute(psql)
    record=cur.fetchall()

    return record

def money_indemnity(start,end):

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f"""select sum(amount),
    sum(amount)/(select sum(amount) from indemnities where creation_date between '{start}' and  '{end}' ),
    refund_status
    from indemnities 
    where creation_date
    between '{start}' and  '{end}' group by refund_status; """)
    cur.execute(psql)
    record=cur.fetchall()

    return record

def money_sinister(start,end):

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f"""select sum(amount),
    sum(amount)/(select sum(amount) from sinisters where creation_date between '{start}' and  '{end}' ),
    status
    from sinisters 
    where creation_date
    between '{start}' and  '{end}' group by status; """)
    cur.execute(psql)
    record=cur.fetchall()
    print(record)
    print(record)
    print(record)
    print(record)
    return record

def statistiques():

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    psql=(
    f"""select count(distinct cl.id),count(distinct sin.extern_id),
        from clients cl
        left join address ad on cl.id= ad.client_id
        left join contracts con on cl.id=con.client_id
        left join sinisters sin on cl.id=sin.client_id
        left join indemnities indem on cl.id=indem.client_id
        """)
    cur.execute(psql)
    record=cur.fetchall()
    
    return record


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)



def envoi_mail_html(subject,template,address_mail,Message,mail):
    
    msg = Message(subject=subject,recipients=[address_mail])
    msg.html=template
    mail.send(msg)

    message='sent mail'
    return message
