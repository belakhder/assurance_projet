from flask import render_template,request,url_for,abort,redirect,flash,session,make_response,json
import uuid
import datetime 
import pdfkit
import os
from main.models.instalments import Instalment

from main.models.payments import Payment 
from utilities_instalments import show_client_instalments,update_instalment,add_payment,search_instalment,search_all_instalment,search_all_instalment,search_one_instalment
from utilities import postgres_connetion,to_csv,time_number
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres
from utilities_client import get_client_by_extern_id
from utilities_company import get_company_by_extern_id
from utilities_contract import get_contract_id
def show_instalments(id,contract_id):
    
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()

        
        columns,columns_names,record=show_client_instalments(id,contract_id,cur)
        
        if record==[]:
            flash('Client Est à Jours Pour Les Paiments ')
            return "<div> Client Est à Jours Pour Les Paiments</div>"
        if request.method=='POST':
            if request.form['submit']=='payer':
            
                f=request.form
                for key in f.keys():

                    if key !='submit':
                        update_instalment(
                            {'status':'Payé','payment_date':str(datetime.datetime.now().date())},
                            id,request.form[key],con,cur)

            submit=request.form['submit']
            

            if submit=='export':
                columns.append('instalment_sum')
                columns.append('total_number')
                
                file_name=f"échéance_{contract_id}"
                all_record,all_columns=search_all_instalment({'extern_contract_id':contract_id,'extern_client_id':id},cur)
                csv=to_csv(file_name,all_columns,all_record)
                response = make_response(csv)
                response.headers["Content-Disposition"] = "attachment; filename=books.csv"
                return response
                
            if submit=='pdf':
                file_name=f"pdf_{contract_id}.pdf"  
                template=render_template(
                "instalments_table.html",search_result=record,columns=columns_names,id=id,contract_id=contract_id)          
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
        "instalment/instalments_client.html",search_result=record,columns=columns_names,id=id,contract_id=contract_id,con=con)


def inst_update(id,contract_id):

    try:
    
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        if request.method=='POST':
            if request.form['submit']=='payer':
                f=request.form
                for key in f.keys():
                    if key !='submit':
                        update_instalment(
                            {'status':'Payé','payment_date':str(datetime.datetime.now().date())},
                            id,request.form[key],con,cur)
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
    return redirect(url_for('instalment.show_all_instalments',id=id,contract_id=contract_id))

def inst_payment(id,contract_id,inst_id):
 
    try:
 
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        
        
        inst_record=search_one_instalment({'extern_id':f"{inst_id}"},cur)
        client_id=get_client_by_extern_id(id,con,cur)
        con_id=get_contract_id(contract_id,con,cur)
        remaining_amount=request.args.get('remaining_amount')
        payment=False
        
        if remaining_amount=='0.0':

            flash(" L'échéance Selectionnée Est  Déja Payé")
            return redirect(url_for('instalment.show_all_instalments',id=id,contract_id=contract_id))
        
        if request.method=='POST' :
            
            if request.form['submit']=='Payer':
                extern_id="pay"+time_number()
                keys="contract_id,client_id,extern_id,extern_client_id,extern_contract_id,inst_id"
                values=[con_id,client_id,extern_id,id,contract_id,inst_id]
                f=request.form
                
                for key in f.keys():
                    if key!='submit'and request.form[key]!='':
                        keys=keys+','+key
                        values.append(str(request.form[key]))
                
                update_dict={'remaining_amount':round(float(request.form['payment_amount']),2)}                
              
                values=tuple(values)

                add_payment(values,keys,con,cur)

                update_instalment(update_dict,id,inst_id,con,cur)
                payment=True
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
    if payment==True:

        return redirect(url_for('instalment.show_all_instalments',id=id,contract_id=contract_id))
    else:
        return render_template('instalment/payment_client.html',id=id,contract_id=contract_id,inst_id=inst_id,remaining_amount=remaining_amount,inst_record=inst_record)



def inst_payment_(id,contract_id,inst_id):
    
    try:
 
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        
        
        inst_record=search_one_instalment({'extern_id':f"{inst_id}"},cur)
        company_id=get_company_by_extern_id(id,con,cur)
        con_id=get_contract_id(contract_id,con,cur)
        remaining_amount=request.args.get('remaining_amount')
        payment=False
        
        if remaining_amount=='0.0':

            flash(" L'échéance Selectionnée Est  Déja Payé")
            return redirect(url_for('instalment.show_all_instalments_',id=id,contract_id=contract_id))
        
        if request.method=='POST' :
            
            if request.form['submit']=='Payer':
                extern_id="pay"+time_number()
                keys="contract_id,company_id,extern_id,extern_client_id,extern_contract_id,inst_id"
                values=[con_id,company_id,extern_id,id,contract_id,inst_id]
                f=request.form
                
                for key in f.keys():
                    if key!='submit'and request.form[key]!='':
                        keys=keys+','+key
                        values.append(str(request.form[key]))
                
                update_dict={'remaining_amount':round(float(request.form['payment_amount']),2)}                
              
                values=tuple(values)
                add_payment(values,keys,con,cur)
                
                update_instalment(update_dict,id,inst_id,con,cur)
                payment=True
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
    if payment==True:

        return redirect(url_for('instalment.show_all_instalments_',id=id,contract_id=contract_id))
    else:
        return render_template('instalment/payment_company.html',id=id,contract_id=contract_id,inst_id=inst_id,remaining_amount=remaining_amount,inst_record=inst_record)


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
       
        count,page_result,columns_names,record=search_instalment(search_dict,page,cur)
        
        link_next=""
        link_previous=""
        max_pages=0
        
       
        if not record:
            flash('Zero Result , Please Check Your Search Criteria !')
            return redirect(url_for('instalment.search_instalments'))  
        else:
            
            next_page=page+1
            previous=page-1
            results=page_result*page
           
            if count%page_result==0:
                max_pages=count//page_result
                
            else:
                file_name=f"search_instalment_result"
                csv_columns = columns_names.copy()

                csv_columns.remove('Link')
                csv_columns.append('number_results')
                
                all_record=search_all_instalment(search_dict,cur)[0]
                to_csv(file_name,csv_columns,all_record)
                
                max_pages=(count//page_result)+1
            
            if results>=count and page==1:
                
                link_next=url_for('instalment.search_result_',search_dict=search_dict_dps,page=1)

            elif page>1 and results>=count:
                link_next=url_for('instalment.search_result_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('instalment.search_result_',search_dict=search_dict_dps,page=next_page)
            if page==1:
             
                
                link_previous=url_for('instalment.search_result_',search_dict=search_dict_dps,page=1)
                
            else:
                link_previous=url_for('instalment.search_result_',search_dict=search_dict_dps,page=previous)

    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_instalments.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)

def searching_instalments():
 
    record=None
    columns_names=None
    if request.method=='POST':
       
        if request.form['submit']=='Chercher':
            try:
                search_dict={}
                client_id=request.form['client_id']
                contract_id=request.form['contract_id']
                status= request.form['status']
                date_type=request.form['date_type']
                daterange=request.form['daterange']
                date1=daterange[0:10].strip()
                date2=daterange[12:].strip()
                
                
                if contract_id and contract_id !='':
                    search_dict['extern_contract_id']=contract_id
                if status and status!='':
                    search_dict['status']=status
         
                if client_id and client_id !='':
                    search_dict['extern_client_id']=client_id
                if daterange !='' and date_type !='':
                    search_dict[f'{date_type}']=f" between '{date1}' and '{date2}'"
                
                search_dict_dps=(json.dumps(search_dict))
                
                return redirect(url_for('instalment.search_result_',search_dict=search_dict_dps,page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
                "search/search_instalments.html",search_result=record,columns=columns_names)


def download_csv(file_name):

    with open(f'csv_file/{file_name}','r') as f:
        csv_file=f.read()
    response = make_response(csv_file)
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    return response

def show_instalments_company(id,contract_id):
    
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()

        
        columns,columns_names,record=show_client_instalments(id,contract_id,cur)
        
        if record==[]:
            flash('Client Est à Jours Pour Les Paiments ')
            return "<div> Client Est à Jours Pour Les Paiments</div>"
        if request.method=='POST':
            if request.form['submit']=='payer':
            
                f=request.form
                for key in f.keys():

                    if key !='submit':
                        update_instalment(
                            {'status':'Payé','payment_date':str(datetime.datetime.now().date())},
                            id,request.form[key],con,cur)

            submit=request.form['submit']
            

            if submit=='export':
                columns.append('instalment_sum')
                columns.append('total_number')
                
                file_name=f"échéance_{contract_id}"
                all_record,all_columns=search_all_instalment({'extern_contract_id':contract_id,'extern_client_id':id},cur)
                csv=to_csv(file_name,all_columns,all_record)
                response = make_response(csv)
                response.headers["Content-Disposition"] = "attachment; filename=books.csv"
                return response
                
            if submit=='pdf':
                file_name=f"pdf_{contract_id}.pdf"  
                template=render_template(
                "instalments_table.html",search_result=record,columns=columns_names,id=id,contract_id=contract_id)          
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
        "instalment/instalments_company.html",search_result=record,columns=columns_names,id=id,contract_id=contract_id,con=con)