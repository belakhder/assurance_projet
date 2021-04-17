
from flask import Flask,render_template,request,url_for,abort,jsonify,redirect,flash,session,json,make_response

from main.models.contract import Contract
from main.models.instalments import Instalment
import uuid
import datetime
from utilities import postgres_connetion,time_number,to_csv,money_contract,money_instalment,money_payment,money_indemnity,money_sinister,add_months
from utilities_contract import update_one_contract_,update_one_contract,insert_one_contract,show_one_contract_info,search_contract_pages,search_contract_pages_export,show_one_contract_info_
from utilities_instalments import insert_one_client_instalments, insert_one_company_instalments
from utilities_payments import add_payment
from utilities_client import get_client_by_extern_id, get_client_id,update_client_info
from utilities_contract import get_contract_id,insert_contract_info_company
from utilities_company import get_company_by_extern_id,update_company_info
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def update_contract(id,contract_id):
    try:
        con=postgres_connetion(
            host_postgres,
            db_name_postgres,
            db_user_postgres,
            db_password_postgres)
        cur=con.cursor() 
    
        client_id=get_client_by_extern_id(id,con,cur)
      
        contract=show_one_contract_info(client_id,contract_id,cur)
        if contract['statu'] in ['Résilié','Annulé']:
            flash(('Pas De modification Possible Contract Cloturé'))
            return redirect(url_for("client.display_client",id=session['client_id'],contract_id=contract_id))
    except Exception as error:
        print(error)
        abort(404)

    if request.method=='POST':
        try:
            update_dict={}
            status=request.form['status']
            if status:
                update_dict['status']=status
                if status=='activated':
                    update_dict['start_date']=str(datetime.datetime.now().date())
                    update_dict['end_date']=str(datetime.datetime.now().date()+datetime.timedelta(days=365))
                if status=='rescinded':
                    update_dict['end_date']=str(datetime.datetime.now().date())
            if update_dict=={}:
                flash('No Modification Is Made')
                return redirect(url_for("client.display_client",id=session['client_id'],contract_id=contract_id))
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
            client_id=get_client_by_extern_id(id,con,cur)
            update_one_contract(update_dict,client_id,contract_id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_client",id=session['client_id'],contract_id=contract_id))

    return render_template("modify_contract.html",id=id,contract_id=contract_id,contract=contract)

def update_contract_(id,contract_id):
    try:
        con=postgres_connetion(
            host_postgres,
            db_name_postgres,
            db_user_postgres,
            db_password_postgres)
        cur=con.cursor() 
    
        company_id=get_company_by_extern_id(id,con,cur)
      
        contract=show_one_contract_info_(company_id,contract_id,cur)
        if contract['statu'] in ['Résilié','Annulé']:
            flash(('Pas De modification Possible Contract Cloturé'))
            return redirect(url_for("client.display_company",id=session['client_id'],contract_id=contract_id))
    except Exception as error:
        print(error)
        abort(404)

    if request.method=='POST':
        try:
            update_dict={}
            status=request.form['status']
            if status:
                update_dict['status']=status
                if status=='activated':
                    update_dict['start_date']=str(datetime.datetime.now().date())
                    update_dict['end_date']=str(datetime.datetime.now().date()+datetime.timedelta(days=365))
                if status=='rescinded':
                    update_dict['end_date']=str(datetime.datetime.now().date())
            if update_dict=={}:
                flash('No Modification Is Made')
                return redirect(url_for("client.display_company",id=session['client_id'],contract_id=contract_id))
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
            company_id=get_company_by_extern_id(id,con,cur)
            update_one_contract_(update_dict,company_id,contract_id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_company",id=session['client_id'],contract_id=contract_id))

    return render_template("contract/modify_contract.html",id=id,contract_id=contract_id,contract=contract)


def add_contract(id):
    if request.method=='POST':
        try:
            price=request.form['price']
            contract_type=request.form['contract_type']
            start_date=request.form['start_date']
            end_date=request.form['end_date']
            nb_inst=int(request.form['nb_inst'])

            payment_amount=request.form.get('payment_amount')
            payment_mode=request.form.get('payment_mode')
            nb_bank_check=request.form.get('nb_bank_check')
            transaction_number=request.form.get('transaction_number')
            card_number=request.form.get('card_number')
            payor_last_name=request.form.get('payor_last_name')
            payor_name=request.form.get('payor_name')
            
            contract_id="ctr"+time_number()
            contract=Contract(
                id=contract_id,price=price,
                contract_type=contract_type,
                start_date=start_date,
                end_date=end_date)
            
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
            client_id=get_client_by_extern_id(id,con,cur)
            insert_one_contract(contract,client_id,con,cur)
            con_id=get_contract_id(contract_id,con,cur)
            due_date=datetime.datetime.now().date()
           
            insts=[]
            if nb_inst!=0:
                inst_amount=round(float(price)/nb_inst,2)
                inst_amount_0=float(price)-(inst_amount*nb_inst)+inst_amount
                inst=Instalment(amount=round(inst_amount_0,2),due_date=str(due_date))
                due_date=due_date+datetime.timedelta(days=30)
                insts.append((inst,"inst"+"0"+time_number()))
                for i in range(1,nb_inst):
                    print(i)
                    inst=Instalment(amount=inst_amount,due_date=str(due_date))
                    due_date=add_months(due_date,1)
                    insts.append((inst,"inst"+f"{i}"+time_number()))
         
                insert_one_client_instalments(insts,client_id,con_id,id,contract_id,con,cur)
    
            else:
                extern_id='pay'+time_number()
                
                keys="extern_contract_id,extern_client_id,extern_id,client_id,contract_id"
                values=[contract_id,id,extern_id,client_id,con_id]
                
                if payment_mode:
                    keys=keys+","+'payment_mode'
                    values.append(payment_mode)   
                if payment_amount:
                    keys=keys+","+'payment_amount'
                    values.append(payment_amount) 
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
                    add_payment(keys,values,con,cur)
            update_client_info({'client_type':'Client'},id,con,cur)
            flash('Listed Successfully ')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_client",id=id,contract_id=contract_id))
        
    return render_template("contract/add_contract.html",id=id,now=str(datetime.datetime.now().date()))

def add_contract_(id):
    if request.method=='POST':
        try:
            price=request.form['price']
            contract_type=request.form['contract_type']
            start_date=request.form['start_date']
            end_date=request.form['end_date']
            nb_inst=int(request.form['nb_inst'])

            payment_amount=request.form.get('payment_amount')
            payment_mode=request.form.get('payment_mode')
            nb_bank_check=request.form.get('nb_bank_check')
            transaction_number=request.form.get('transaction_number')
            card_number=request.form.get('card_number')
            payor_last_name=request.form.get('payor_last_name')
            payor_name=request.form.get('payor_name')
            
            contract_id="ctr"+time_number()
            contract=Contract(
                id=contract_id,price=price,
                contract_type=contract_type,
                start_date=start_date,
                end_date=end_date)
            
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

            company_id=get_company_by_extern_id(id,con,cur)
            insert_contract_info_company(contract,company_id,con,cur)
            con_id=get_contract_id(contract_id,con,cur)
            due_date=datetime.datetime.now().date()
           
            insts=[]
            if nb_inst!=0:
                inst_amount=round(float(price)/nb_inst,2)
                inst_amount_0=float(price)-(inst_amount*nb_inst)+inst_amount
                inst=Instalment(amount=round(inst_amount_0,2),due_date=str(due_date))
                due_date=due_date+datetime.timedelta(days=30)
                insts.append((inst,"inst"+"0"+time_number()))
                for i in range(1,nb_inst):
                    print(i)
                    inst=Instalment(amount=inst_amount,due_date=str(due_date))
                    due_date=add_months(due_date,1)
                    insts.append((inst,"inst"+f"{i}"+time_number()))
         
                insert_one_company_instalments(insts,company_id,con_id,id,contract_id,con,cur)
    
            else:
                extern_id='pay'+time_number()
                
                keys="extern_contract_id,extern_client_id,extern_id,company_id,contract_id"
                values=[contract_id,id,extern_id,company_id,con_id]
                
                if payment_mode:
                    keys=keys+","+'payment_mode'
                    values.append(payment_mode)   
                if payment_amount:
                    keys=keys+","+'payment_amount'
                    values.append(payment_amount) 
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
                    add_payment(keys,values,con,cur)
            update_company_info({'company_type':'Client'},id,con,cur)
            flash('Listed Successfully ')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_company",id=id,contract_id=contract_id))
        
    return render_template("contract/add_contract.html",id=id,now=str(datetime.datetime.now().date()))


def searching_contract_():
    
    record=None
    columns_names=None
    if request.method=='POST':
        print(request.form)
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
                        "search/search_contract.html",search_result=record,columns=columns_names)

                return redirect(url_for('contract.get_search_contract_',search_dict=json.dumps(search_dict),page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
        "search/search_contract.html",search_result=record,columns=columns_names,now=str(datetime.datetime.now().date()))

def get_searching_contract():
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
        
        count,page_result,columns_names,record=search_contract_pages(search_dict,page,cur)
        
        
        link_next=""
        link_previous=""
        max_pages=0
        if not record:
            redirect('contract.search_contract_')
            flash('Zero Result , Please Check Your Search Criteria !')
        else :
            file_name=f"search_result"
            csv_columns = columns_names.copy()
            csv_columns.insert(0,'id')
            csv_columns.remove('Link')
            csv_columns.append('contracts')
            csv_columns.append('nombre de resultat')
            record2=search_contract_pages_export(search_dict,page,cur)
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
                
                link_next=url_for('contract.get_search_contract_',search_dict=search_dict_dps,page=1)
                
            elif page>1 and results>=count:
                link_next=url_for('contract.get_search_contract_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('contract.get_search_contract_',search_dict=search_dict_dps,page=next_page)
            if page==1:
                link_previous=url_for('contract.get_search_contract_',search_dict=search_dict_dps,page=1)
            else:
                link_previous=url_for('contract.get_search_contract_',search_dict=search_dict_dps,page=previous)

    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_contract.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,now=str(datetime.datetime.now().date()))




def download_csv(file_name):

    with open(f'csv_file/{file_name}','r') as f:
        csv_file=f.read()
    response = make_response(csv_file)
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response


def moneys_contract():
    record=record=money_contract(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record2=money_instalment(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record3=money_payment(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record4=money_indemnity(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record5=money_sinister(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    date1=add_months(datetime.datetime.now().date(),-1).strftime("%d-%m-%Y")
    date2=(datetime.datetime.now().date()).strftime("%d-%m-%Y")
    date={}
    if request.method=='POST':
        
        daterange_con=request.form['daterange_con']
        daterange_pay=request.form['daterange_pay']
        daterange_sin=request.form['daterange_sin']
        daterange_indem=request.form['daterange_indem']
        daterange_inst=request.form['daterange_inst']
        
        
        if daterange_con:
            record=money_contract(daterange_con[0:10].strip(),daterange_con[12:].strip())
            date['date1']=((daterange_con[0:10].strip(),daterange_con[12:].strip()))
        if daterange_inst:
            record2=money_instalment(daterange_inst[0:10].strip(),daterange_inst[12:].strip())
            date['date2']=((daterange_inst[0:10].strip(),daterange_inst[12:].strip()))
        if daterange_pay:
            record3=money_payment(daterange_pay[0:10].strip(),daterange_pay[12:].strip())
            date['date3']=((daterange_pay[0:10].strip(),daterange_pay[12:].strip()))
        if daterange_indem :
            record4=money_indemnity(daterange_indem[0:10].strip(),daterange_indem[12:].strip())
            date['date4']=((daterange_indem[0:10].strip(),daterange_indem[12:].strip()))
        if daterange_sin:
            record5=money_sinister(daterange_sin[0:10].strip(),daterange_sin[12:].strip())
            date['date5']=((daterange_indem[0:10].strip(),daterange_indem[12:].strip()))
    return render_template('dashbord/dashbord_contract.html',record=record,record2=record2,record3=record3,record4=record4,record5=record5,date1=date1,date2=date2,date=date)

