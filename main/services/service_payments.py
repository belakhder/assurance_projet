from utilities_instalments import search_one_instalment
from flask import render_template,request,url_for,abort,redirect,flash,session,make_response,json
import uuid
import datetime 
import pdfkit
import os

from main.models.payments import Payment 
from utilities_payments import show_client_payments,update_payment,add_payment,search_payment,search_all_payment
from utilities import postgres_connetion,to_csv,time_number
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres


#unused
def show_payments(id,contract_id):
    
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()

        
        columns,columns_names,record=show_client_payments(id,contract_id,cur)
        
        if request.method=='POST':
            if request.form['submit']=='payer':
            
                f=request.form
                for key in f.keys():
                    if key !='submit':
                        update_payment(
                            {'status':'Payé','payment_date':str(datetime.datetime.now().date())},
                            id,request.form[key],con,cur)
            submit=request.form['submit']
            
            if submit=='export':
                columns.append('payment_sum')
                columns.append('total_number')
                
                file_name=f"échéance_{contract_id}"
                csv=to_csv(file_name,columns,record[:-3])
                response = make_response(csv)
                response.headers["Content-Disposition"] = "attachment; filename=books.csv"
                return response
            if submit=='pdf':
                file_name=f"pdf_{contract_id}.pdf"  
                template=render_template(
                "payments_table.html",search_result=record,columns=columns_names,id=id,contract_id=contract_id)          
                main_dir=os.path.basename(os.path.dirname(os.path.dirname(__file__)))
                css1=os.path.join(main_dir,"static","css","bootstrap.min.css")
                css2=os.path.join(main_dir,"static","css","bootstrap.css")
                css=[css1,css2]
                pdf=pdfkit.from_string(template,False,css=css)
                response= make_response(pdf)
                response.headers['Content-type']='application/pdf'
                response.headers['Content-disposition']=f'inline;filename={file_name}'
                return response
            
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "payments.html",search_result=record,columns=columns_names,id=id,contract_id=contract_id)

#unused
def inst_update(id,contract_id):
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        
        #search_one_instalment({'extern_id'=f"{id}"})
        if request.method=='POST':
            if request.form['submit']=='payer':
                f=request.form
                for key in f.keys():
                    if key !='submit':
                        update_payment(
                            {'status':'Payé','payment_date':str(datetime.datetime.now().date())},
                            id,request.form[key],con,cur)
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
    return redirect(url_for('payment.show_all_payments',id=id,contract_id=contract_id))

#unused
def inst_payment(id,contract_id,inst_id):
    
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        inst_record=search_one_instalment({'extern_id':f"{inst_id}"},cur)
        print('inst_record')
        remaining_amount=request.args.get('remaining_amount')
        payment=False
        
        if remaining_amount=='0.0':

            flash(" L'échéance Selectionnée Est  Déja Payé")
            return redirect(url_for('payment.show_all_payments',id=id,contract_id=contract_id))

        if request.method=='POST':
            
            if request.form['submit']=='Payer':
                extern_id="pay"+time_number()
                keys="client_id,contract_id,inst_id,extern_id"
                values=[id,contract_id,inst_id,extern_id]
                f=request.form
                for key in f.keys():
                    if key!='submit'and request.form[key]!='':
                        keys=keys+','+key
                        values.append(str(request.form[key]))
                update_dict={'remaining_amount':round(request.form['amount'],2)}                
              
                values=tuple(values)
                
               
                add_payment(values,keys,con,cur)
                update_payment(update_dict,id,inst_id,con,cur)
                payment=True
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
    if payment==True:

        return redirect(url_for('payment.show_all_payments',id=id,contract_id=contract_id))
    else:
        return render_template('paiement.html',id=id,contract_id=contract_id,inst_id=inst_id,remaining_amount=remaining_amount,inst_record=inst_record)

def search_result():

    search_dict_dps=request.args.get('search_dict',{})
    search_dict= json.loads(request.args.get('search_dict',{}))

    page= int(request.args.get('page', 1))
    try:
        con=postgres_connetion(
            host_postgres,
            db_name_postgres,
            db_user_postgres,
            db_password_postgres)
        cur=con.cursor()
        
        count,page_result,columns_names,record=search_payment(search_dict,page,cur)
        
        link_next=""
        link_previous=""
        max_pages=0
        
        if not record:
            redirect('payment.search_result_')
            
            flash('Zero Result , Please Check Your Search Criteria !')
        else:
            file_name=f"search_payment_result"
            csv_columns = columns_names.copy()
            csv_columns.insert(0,'id')
            csv_columns.remove('Link')
            
            all_record=search_all_payment(search_dict,cur)
            to_csv(file_name,csv_columns,all_record)

            next_page=page+1
            previous=page-1
            results=page_result*page
            print(count)
            if count%page_result==0:
                max_pages=count//page_result
                
            else:
                
                max_pages=(count//page_result)+1
            
            if results>=count and page==1:
                
                link_next=url_for('payment.search_result_',search_dict=search_dict_dps,page=1)
             
            elif page>1 and results>=count:
                link_next=url_for('payment.search_result_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('payment.search_result_',search_dict=search_dict_dps,page=next_page)
            if page==1:
             
                
                link_previous=url_for('payment.search_result_',search_dict=search_dict_dps,page=1)
                
            else:
                link_previous=url_for('payment.search_result_',search_dict=search_dict_dps,page=previous)
            
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_payments.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=5,max_pages=max_pages,now=str(datetime.datetime.now().date()))

def searching_payments():
 
    record=None
    columns_names=None
    if request.method=='POST':
        
        if request.form['submit']=='Chercher':
            
            try:
                search_dict={}
                client_id=request.form['client_id']
                contract_id=request.form['contract_id']
                Payment_mode=request.form['Payment_mode']
                nb_bank_check=request.form['nb_bank_check']
                transaction_number =request.form['transaction_number']
                card_number =request.form['card_number']
                payor_last_name =request.form['payor_last_name']
                payor_name=request.form['payor_name']
                daterange=request.form['daterange']
                date_type=request.form['date_type']
                date1=daterange[0:10].strip()
                date2=daterange[12:].strip()

                if contract_id and contract_id !='':
                    search_dict['extern_contract_id']=contract_id
                if Payment_mode and Payment_mode!='':
                    search_dict['Payment_mode']=Payment_mode                
                
                if nb_bank_check and nb_bank_check!='':
                    search_dict['nb_bank_check']=nb_bank_check           
                if transaction_number and transaction_number!='':
                    search_dict['transaction_number']=nb_bank_check                 
                if card_number and card_number !='':
                    search_dict['card_number']=card_number               
                if payor_last_name and payor_last_name !='':
                    search_dict['payor_last_name']=payor_last_name                 
                if payor_name and payor_name !='':
                    search_dict['payor_name']=payor_name                
                if client_id and client_id !='':
                    search_dict['extern_client_id']=client_id
                if daterange !='' and date_type !='' :
                    search_dict[f'{date_type}']=f" between '{date1}' and '{date2}'"
                
                search_dict_dps=(json.dumps(search_dict))
                print('lkjhmjc<smxclk<nxw')
                return redirect(url_for('payment.search_result_',search_dict=search_dict_dps,page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
                "search/search_payments.html",search_result=record,columns=columns_names)

def download_csv(file_name):
    with open(f'csv_file/{file_name}','r') as f:
        csv_file=f.read()
    response = make_response(csv_file)
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response