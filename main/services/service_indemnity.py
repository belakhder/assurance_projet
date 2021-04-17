
from flask import Flask,render_template,request,url_for,abort,jsonify,redirect,flash,session,json

from main.models.sinister import Sinister
import uuid
import datetime 
from utilities import postgres_connetion,to_csv
from utilities_indemnity import update_one_indemnity,check_indemnity_status,search_indemnity,search_indemnity_export,indemnity_to_update
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def update_indemnity(id,indemnity_id):

    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    indemnity=indemnity_to_update(indemnity_id,con,cur)
    if request.method=='POST':
        
        try:
            
            refund_status=request.form['refund_status']
            
            update_dict={}
            
            if  refund_status:
                update_dict['refund_status']= refund_status
                
            if update_dict=={}:
                flash('No Modification Is Made')
                
                return redirect(url_for('client.display_client',id=session['client_id'],contract_id=session['contract_id']))

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
            check=check_indemnity_status(id,indemnity_id,con,cur)

            if check:
                flash("Can't Update Indemnity ,Customer Has Already Received His Refund! ")
            else:
                update_one_indemnity(update_dict,id,indemnity_id,con,cur)

                flash('Updated Sucessfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for('client.display_client',id=session['client_id'],contract_id=session['contract_id']))
        
    return render_template("indemnity/modify_indemnity.html",id=id,indemnity_id=indemnity_id,indemnity=indemnity)

def update_indemnity_(id,indemnity_id):
   
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    indemnity=indemnity_to_update(indemnity_id,con,cur)

    if request.method=='POST':
        
        try:
            
            refund_status=request.form['refund_status']
            
            update_dict={}
            
            if  refund_status:
                update_dict['refund_status']= refund_status
                
            if update_dict=={}:
                flash('No Modification Is Made')
                
                return redirect(url_for('client.display_company',id=session['client_id'],contract_id=session['contract_id']))

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
            check=check_indemnity_status(id,indemnity_id,con,cur)

            if check:
                flash("Can't Update Indemnity ,Customer Has Already Received His Refund! ")
            else:
                update_one_indemnity(update_dict,id,indemnity_id,con,cur)

                flash('Updated Sucessfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for('client.display_company',id=session['client_id'],contract_id=session['contract_id']))
        
    return render_template("indemnity/modify_indemnity.html",id=id,indemnity_id=indemnity_id,indemnity=indemnity)



def searching_indemnities():
 
    record=None
    columns_names=None
    if request.method=='POST':
    
        if request.form['submit']=='Chercher':
            try:
                search_dict={}
                
                refund_status= request.form['refund_status']
                amount=request.form['amount']
                client_id=request.form['client_id']
                date_type=request.form['date_type']
                daterange=request.form['daterange']
                date1=daterange[0:10].strip()
                date2=daterange[12:].strip()


                if refund_status and refund_status!='':
                    search_dict['refund_status']=refund_status
                if amount and amount!='':
                    search_dict['amount']=amount            
                if client_id and client_id !='':
                    search_dict['extern_client_id']=client_id
                if daterange !='' and date_type !='':
                    search_dict[f'{date_type}']=f" between '{date1}' and '{date2}'"
                
                search_dict_dps=(json.dumps(search_dict))
                return redirect(url_for('indemnity.search_result_',search_dict=search_dict_dps,page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
                "search/search_indemnities.html",search_result=record,columns=columns_names)

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
        
        count,page_result,columns_names,record=search_indemnity(search_dict,page,cur)
        print(record)
        link_next=""
        link_previous=""
        max_pages=0
        if not record:
            redirect('indemnity.search_result_')
            flash('Zero Result , Please Check Your Search Criteria !')
        else:
            file_name=f"search_indemnity_result"
            csv_columns = columns_names.copy()
            csv_columns.insert(0,'id')
            csv_columns.remove('Link')
            csv_columns.append('nombre de resultat')
            record2=search_indemnity_export(search_dict,page,cur)
            to_csv(file_name,csv_columns,record2)
            
            next_page=page+1
            previous=page-1
            results=page_result*page

            if count%page_result==0:
                max_pages=count//page_result
                
            else:
                max_pages=(count//page_result)+1
                

            if results>=count and page==1:
                
                link_next=url_for('indemnity.search_result_',search_dict=search_dict_dps,page=1)
            
            elif page>1 and results>=count:
                link_next=url_for('indemnity.search_result_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('indemnity.search_result_',search_dict=search_dict_dps,page=next_page)
            if page==1:
            
                
                link_previous=url_for('indemnity.search_result_',search_dict=search_dict_dps,page=1)
                
            else:
                link_previous=url_for('indemnity.search_result_',search_dict=search_dict_dps,page=previous)
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_indemnities.html",search_result=record,columns=columns_names,
        search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)
