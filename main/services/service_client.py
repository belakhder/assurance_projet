
from flask import Flask,render_template,request,url_for,abort,jsonify,redirect,flash,session,g,json,make_response
import requests
from main.models.address import Address
from main.models.contract import Contract
from main.models.client import Client
from main.models.sinister import Sinister
from main.models.instalments import Instalment
from main.models.company import Company
import uuid
import smtplib
import psycopg2
from flask import current_app
from psycopg2.errors import UniqueViolation
import datetime 
from utilities import postgres_connetion,time_number,to_csv
from utilities_client import insert_client_info,search_client,search_fiche_client,update_client_info,get_all_client,search_client_pages,client_to_update,search_client_pages_export,get_client_id,insert_client_info_payment
from utilities_instalments import add_payment
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres,default_country_name
from utilities_instalments import insert_one_client_instalments ,insert_one_company_instalments
from utilities_address import  insert_address_info, insert_address_info_company
from utilities_contract import  insert_contract_info,get_contract_id, insert_contract_info_company
from utilities_company import  insert_company_info,get_company_id
from flask_mail import Mail
from flask_mail import Message
from smtplib import SMTPResponseException

# a supprimer
def searching_client():
    
    record=None
    columns_names=None
    if request.method=='POST':
    
        if request.form['submit']=='Search':
            try:
                search_dict={}
                client_reference=request.form['client_reference']
                name= request.form['first_name']
                last_name=request.form['last_name']
                email=request.form['email']
                tel=request.form['tel']
                contract_type=request.form['contract_type']
                contract_reference=request.form['contract_reference']
                status=request.form['status']
                

                if client_reference and client_reference!='':
                    search_dict['cl.extern_id']=client_reference
                if name and name!='':
                    search_dict['name']=name
                if last_name and last_name!='':
                    search_dict['last_name']=last_name
                if email and email!='':
                    search_dict['email']=email
                if tel and tel!='':
                    search_dict['tel']=tel            

                if contract_type and contract_type !='':
                    search_dict['contract_type']=contract_type
                if contract_reference and contract_reference !='':
                    search_dict['con.extern_id']=contract_reference
                if status and status!='':
                    search_dict['status']=status
                
               
            except Exception as error:
                print(error)
                abort(400)
            try:
                con=postgres_connetion(
                    host_postgres,
                    db_name_postgres,
                    db_user_postgres,
                    db_password_postgres)
                cur=con.cursor()

                columns_names,record=search_client(search_dict,cur)
                if not record:
                    flash('Zero Result , Please Check Your Search Criteria !')
            except Exception as error:
                print(error)
                abort(422)
            finally :
                if con is not None:
                    cur.close()
                    con.close()

    return render_template(
        "search/search_client.html",search_result=record,columns=columns_names)


def client_subscription():
    abort(404)
    if request.method=='POST':
        
        print(request.form)
        con=None
        nb_inst=None
        try:
            register=False
            contract_id="ctr"+time_number()
            id_address='adr'+time_number()
            name= request.form['first_name']
            last_name=request.form['last_name']
            email=request.form['email']
            
            client_type=request.form['client_type']
            
            tel=request.form['full_number']
            line1=request.form['line1']
            line2=request.form['line2']
            city=request.form['city']
            postal_code=request.form['postal_code']
            country=request.form['country']
            state=request.form['state']
            price=request.form.get('price')
            contract_type=request.form.get('contract_type')
            start_date=request.form.get('start_date')
            
            end_date=request.form.get('end_date')

            id=name[0]+last_name[0:2]+time_number()
            
            
            payment_amount=request.form.get('payment_amount')
            payment_mode=request.form.get('payment_mode')
            nb_bank_check=request.form.get('nb_bank_check')
            transaction_number=request.form.get('transaction_number')
            card_number=request.form.get('card_number')
            payor_last_name=request.form.get('payor_last_name')
            payor_name=request.form.get('payor_name')
            nb_inst=request.form.get('nb_inst')
                                    
            if country=='':
                country=default_country_name
            if request.form.get('nb_inst')!='0':
                nb_inst=int(request.form.get('nb_inst'))
            address=Address(
                id=id_address,
                line1=line1,
                line2=line2,
                city=city,
                postal_code=postal_code,
                state=state,
                country=country)
            if price=='':
                contract=None
            else :
                contract=Contract(id=contract_id,price=float(price),contract_type=contract_type,start_date=start_date,end_date=end_date)
            client=Client(id=id,name=name,last_name=last_name,email=email,tel=tel,client_type=client_type,address=address)
            
        except Exception as error:
            print(error)
            abort(400)
        try:
            con=postgres_connetion(
                host_postgres,
                db_name_postgres,
                db_user_postgres,
                db_password_postgres)
            cur=con.cursor()
            if client_type =='Client Potentiel':
                insert_client_info(client,con,cur)
                client_id=get_client_id(email,con,cur)
                print(client_id)
                session.client_sub_id=client_id
                insert_address_info(address,client_id,id,con,cur)
                register=True
                contract_id='ClientPotentiel'
                

            else :       
                due_date=datetime.datetime.now().date()
                insts=[]
                
                if nb_inst!='0':
                    
                    insert_client_info(client,con,cur)
                    client_id=get_client_id(email,con,cur)
                    print(client_id)
                    session.client_sub_id=client_id
                    insert_address_info(address,client_id,id,con,cur)
                    insert_contract_info(contract,client_id,con,cur)
                    ctr_id=get_contract_id(contract_id,con,cur)
                    inst_amount=round(float(price)/nb_inst,2)
                    
                    for i in range(nb_inst):

                        inst=Instalment(amount=inst_amount,due_date=str(due_date))
                        due_date=due_date+datetime.timedelta(days=30)
                        insts.append((inst,"inst"+f"{i}"+time_number()))

                    insert_one_client_instalments(insts,client_id,ctr_id,id,contract_id,con,cur)
                    
                else:
                    insert_client_info(client,con,cur)
                    client_id=get_client_id(email,con,cur)
                    session.client_sub_id=client_id
                    insert_address_info(address,client_id,id,con,cur)
                    insert_contract_info(contract,client_id,con,cur)
                    ctr_id=get_contract_id(contract_id,con,cur)
                    
                    keys="client_id,contract_id,extern_id,extern_client_id,extern_contract_id"
                    values=[client_id,ctr_id,'pay'+time_number(),id,contract_id]
                    if payment_amount:
                        keys=keys+","+'payment_amount'
                        values.append(payment_amount)
                    if payment_mode:
                        keys=keys+","+'payment_mode'
                        values.append(payment_mode)   
                    if nb_bank_check:
                        keys=keys+","+'nb_bank_check'
                        values.append(nb_bank_check)   
                    if transaction_number:
                        keys=keys+","+'transaction_number'
                        values.append(transaction_number) 
                    if card_number:
                        keys=keys+","+'card_number'
                        values.append(card_number) 

                    if payor_last_name:
                        keys=keys+","+'payor_last_name'
                        values.append(payor_last_name)
                    if payor_name:
                        keys=keys+","+'payor_name'
                        values.append(payor_name)
                    values=tuple(values)
                    if keys!='client_id,contract_id,payment_mode':
                        insert_client_info_payment(keys,values,con,cur)
                    else:
                        flash('Paiement Non Enregistré')
                register=True
                flash('Subscription Successfully Made')
        except (Exception, psycopg2.Error) as error:
            print(error)
            print('hello7')
            register=False
            if  isinstance(error,UniqueViolation):
                flash('Chosen Information Already Existe')
            else:
                abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        if register== True :
            return redirect(url_for("client.display_client",id=id,contract_id=contract_id))

    return render_template("client/souscription_client.html",now=str(datetime.datetime.now().date()))



def display_one_client(id,contract_id):
 
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        [client_info,contracts,address_info,sinisters,indemnity,total_indemnity,record,unpaid,relance,nb]=search_fiche_client(id,contract_id,cur)
    
        session['client_id']=client_info['id']
        session['contract_id']=contract_id
    except Exception as error:
        print(error) 
        abort(422)

    finally :
        if con is not None:
            cur.close()
            con.close()
    if not record:
        abort(400)

    return render_template("client/fiche_client.html" ,
        client_info=client_info ,
        address_info=address_info,
        data=json.dumps(sinisters),
        contracts=contracts,
        sinisters_history=sinisters,
        indemnity=indemnity,
        total_indemnity=total_indemnity,
        unpaid=unpaid,
        relance=relance,
        message='client est à jours',
        id=id,
        nb=nb,
        contract_id=contract_id
        )

def update_clients_info(id):
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()   
    client=client_to_update(id,con,cur)
    if request.method== 'POST':
        error=True
        try:
            update_dict={}

            email=request.form['email']
            tel=request.form['tel']
            if email:
                update_dict['email']=email
            if tel:
                update_dict['tel']=tel
            if update_dict=={}:
                flash('no modification is made')
                return redirect(url_for("client.display_client",id=session['client_id'],contract_id=session['contract_id']))
                

        except Exception as error:
            print(error)
            abort(400)

        try:
            con=postgres_connetion(
                host_postgres,
                db_name_postgres,
                db_user_postgres,
                db_password_postgres)
            cur=con.cursor()      

            update_client_info(update_dict,id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_client",id=session['client_id'],contract_id=session['contract_id']))

    return render_template("client/modify_client_info.html",id=id,client=client)


def display_all_client():
    try:

        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
       
        page= int(request.args.get('page', 1))
        
        count,page_result,columns_names,record=get_all_client(page,cur)
        
        next_page=page+1
        previous=page-1
        results=page_result*page
        max_pages=count//page_result
     
        

        if record:
            if count%page_result==0:
                max_pages=count//page_result
            else:
                max_pages=(count//page_result)+1
            
            if results>=count and page==1:
                link_next=url_for('client.get_all_clients',page=1)
            elif page>1 and results>=count:
                link_next=url_for('client.get_all_clients',page=page)
            else:
                link_next=url_for('client.get_all_clients',page=next_page)
            if page==1:
                link_previous=url_for('client.get_all_clients',page=1)
            else:
                link_previous=url_for('client.get_all_clients',page=previous)
        print(hhj)
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
        if not record :
            flash("vous n'avez pas encore de clients souscrits" )
            return redirect(url_for('client.subscription'))
        else:
            return render_template(
                "client/clients.html",search_result=record,columns=columns_names,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)


def searching_client_():
    
    record=None
    columns_names=None
    if request.method=='POST':
    
        if request.form['submit']=='Chercher':
            try:
                search_dict={}
                client_reference=request.form['client_reference']
                name= request.form['first_name']
                last_name=request.form['last_name']
                email=request.form['email']
                tel=request.form['tel']
                contract_type=request.form['contract_type']
                contract_reference=request.form['contract_reference']
                status=request.form['status']
                date_type=request.form['date_type']
                daterange=request.form['daterange']
                date1=daterange[0:10].strip()
                date2=daterange[12:].strip()


                if client_reference and client_reference!='':
                    search_dict['extern_id']=client_reference
                if name and name!='':
                    search_dict['name']=name
                if last_name and last_name!='':
                    search_dict['last_name']=last_name
                if email and email!='':
                    search_dict['email']=email
                if tel and tel!='':
                    search_dict['tel']=tel            
                if contract_type and contract_type !='':
                    search_dict['contract_type']=contract_type
                if contract_reference and contract_reference !='':
                    search_dict['con.extern_id']=contract_reference
                if status and status!='':
                    search_dict['status']=status
                if daterange !='' and date_type!='' :
                    search_dict[f'{date_type}']=f" between '{date1}' and '{date2}'"
                if search_dict=={}:
                    flash('Please Enter At Least One Field')
                    return render_template(
                        "search/search_client.html",search_result=record,columns=columns_names)

                return redirect(url_for('client.get_search_client_',search_dict=json.dumps(search_dict),page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
        "search/search_client.html",search_result=record,columns=columns_names,now=str(datetime.datetime.now().date()))

def get_searching_client():
    search_dict_dps=(request.args.get('search_dict', 1))
    search_dict=json.loads(request.args.get('search_dict', 1))
    page= int(request.args.get('page', 1))
    try:
        
        con=postgres_connetion(
            host_postgres,
            db_name_postgres,
            db_user_postgres,
            db_password_postgres)
        cur=con.cursor()
        
        count,page_result,columns_names,record=search_client_pages(search_dict,page,cur)
        
        
        link_next=""
        link_previous=""
        max_pages=0
        if not record:
            redirect('client.search_client_')
            flash('Zero Result , Please Check Your Search Criteria !')
        else :
            file_name=f"search_result"
            csv_columns = columns_names.copy()

            csv_columns.remove('Link')
            csv_columns.append('contracts')
            csv_columns.append('number_results')
            record2=search_client_pages_export(search_dict,page,cur)
            to_csv(file_name,csv_columns,record2)

            next_page=page+1
            previous=page-1
            results=page_result*page
            max_pages=count//page_result
            if count%page_result==0:
                max_pages=count//page_result
                
            else:

                max_pages=max_pages+1

            if results>=count and page==1:
                
                link_next=url_for('client.get_search_client_',search_dict=search_dict_dps,page=1)
                
            elif page>1 and results>=count:
                link_next=url_for('client.get_search_client_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('client.get_search_client_',search_dict=search_dict_dps,page=next_page)
            if page==1:
                link_previous=url_for('client.get_search_client_',search_dict=search_dict_dps,page=1)
            else:
                link_previous=url_for('client.get_search_client_',search_dict=search_dict_dps,page=previous)

    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_client.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,now=str(datetime.datetime.now().date()))




def download_csv(file_name):

    with open(f'csv_file/{file_name}','r') as f:
        csv_file=f.read()
    response = make_response(csv_file)
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response
    
    


def company_subscription():
    print(request.form)
    
    if request.method=='POST':

        con=None
        nb_inst=None
        try:
            register=False
            contract_id='s'+"ctr"+time_number()+'s'
            id_address='s'+'adr'+time_number()+'s'
            company_name= request.form['company_name']
            company_email=request.form['company_email']
            client_type=request.form['client_type']
            company_tel=request.form['full_number']
            
            line1=request.form['line1']
            line2=request.form['line2']
            city=request.form['city']
            postal_code=request.form['postal_code']
            country=request.form['country']
            state=request.form['state']
            
            company_registration_nb=request.form['company_registration_nb']
            price=request.form.get('price')
            contract_type=request.form.get('contract_type')
            start_date=request.form.get('start_date')
            
            end_date=request.form.get('end_date')
            id='s'+company_name[0:3]+time_number()
            payment_amount=request.form.get('payment_amount')
            payment_mode=request.form.get('payment_mode')
            nb_bank_check=request.form.get('nb_bank_check')
            transaction_number=request.form.get('transaction_number')
            card_number=request.form.get('card_number')
            payor_last_name=request.form.get('payor_last_name')
            payor_name=request.form.get('payor_name')
            nb_inst=request.form.get('nb_inst')
            
            if country=='':
                country=default_country_name
            if request.form.get('nb_inst')!='0':
                nb_inst=int(request.form.get('nb_inst'))

            address=Address(
                id=id_address,
                line1=line1,
                line2=line2,
                city=city,
                postal_code=postal_code,
                state=state,
                country=country)
            if price=='':
                contract=None
            else :
                contract=Contract(id=contract_id,price=float(price),contract_type=contract_type,start_date=start_date,end_date=end_date)
            company=Company(id=id,company_name=company_name,company_email=company_email,company_tel=company_tel,company_registration_nb=company_registration_nb,company_type=client_type,address=address)
            
        except Exception as error:
            print(error)
            abort(400)
        try:
            con=postgres_connetion(
                host_postgres,
                db_name_postgres,
                db_user_postgres,
                db_password_postgres)
            cur=con.cursor()

            if client_type =='Client Potentiel':
                insert_company_info(company,con,cur)
                company_id=get_company_id(company_email,con,cur)
                print(company_id)
                session.company_sub_id=company_id
                insert_address_info_company(address,company_id,id,con,cur)
                register=True
                contract_id='ClientPotentiel'
            else :
                due_date=datetime.datetime.now().date()
                insts=[]

                
                if nb_inst!='0':
                    
                    insert_company_info(company,con,cur)
                    company_id=get_company_id(company_email,con,cur)
                    print(company_id)
                    session.company_sub_id=company_id
                    insert_address_info_company(address,company_id,id,con,cur)
                    insert_contract_info_company(contract,company_id,con,cur)
                    ctr_id=get_contract_id(contract_id,con,cur)
                    inst_amount=round(float(price)/nb_inst,2)
                    
                    for i in range(nb_inst):

                        inst=Instalment(amount=inst_amount,due_date=str(due_date))
                        due_date=due_date+datetime.timedelta(days=30)
                        insts.append((inst,"inst"+f"{i}"+time_number()))

                    insert_one_company_instalments(insts,company_id,ctr_id,id,contract_id,con,cur)
                    
                else:
                    insert_company_info(company,con,cur)
                    print(company_email)
                    company_id=get_company_id(company_email,con,cur)
                    print(company_id)
                    
                    session.company_sub_id=company_id
                    insert_address_info_company(address,company_id,id,con,cur)
                    
                    insert_contract_info_company(contract,company_id,con,cur)
                    ctr_id=get_contract_id(contract_id,con,cur)
                    
                    keys="company_id,contract_id,extern_id,extern_client_id,extern_contract_id"
                    values=[company_id,ctr_id,'pay'+time_number(),id,contract_id]
                    if payment_amount:
                        keys=keys+","+'payment_amount'
                        values.append(payment_amount)
                    if payment_mode:
                        keys=keys+","+'payment_mode'
                        values.append(payment_mode)   
                    if nb_bank_check:
                        keys=keys+","+'nb_bank_check'
                        values.append(nb_bank_check)   
                    if transaction_number:
                        keys=keys+","+'transaction_number'
                        values.append(transaction_number) 
                    if card_number:
                        keys=keys+","+'card_number'
                        values.append(card_number) 
                    if payor_last_name:
                        keys=keys+","+'payor_last_name'
                        values.append(payor_last_name)
                    if payor_name:
                        keys=keys+","+'payor_name'
                        values.append(payor_name)
                    values=tuple(values)
                    
                    if keys!='company_id,contract_id,payment_mode':
                        print('hello5')
                        insert_client_info_payment(keys,values,con,cur)
                        print('gejkjnwdkjcnwkcjnwkjnwkxjc')
                    else:
                        flash('Paiement Non Enregistré')
                register=True
                flash('Subscription Successfully Made')
            try:
                with current_app.app_context():
                    template=render_template(
                    "mail_confirmation.html")
                    mail = Mail()
                
                    msg = Message("Hello",
                                sender="belakhder.fathi@gmail.com",
                                recipients=[company_email])
                    msg.html=template
                    mail.send(msg)
            except (Exception,smtplib.SMTPResponseException) as  error:
                print(error)
                abort(422)
                
                flash('confirmation non envoyé svp vérifiez votre mail')
        except (Exception, psycopg2.Error) as error:
            print(error)
            register=False
            if  isinstance(error,UniqueViolation):
                flash('Chosen Information Already Existe')
            else:
                abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        if register== True :
           
            return redirect(url_for("client.display_company",id=id,contract_id=contract_id))

    return render_template("company/souscription_company.html",now=str(datetime.datetime.now().date()))


def error_422_handler_search():
    flash('Erreur innatendue')
    return render_template("search/search_client.html")