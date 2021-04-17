
from utilities_client import get_client_by_extern_id
from flask import Flask,render_template,request,url_for,abort,jsonify,redirect,flash,session,json

from main.models.sinister import Sinister
from main.models.indemnity import Indemnity
import uuid
import datetime 
from utilities import postgres_connetion,time_number,to_csv
from utilities_sinister import add_sinister_,add_sinister,update_one_sinister,sinister_to_update,search_sinister,update_one_modifications,add_modification,count_modification,search_all_sinister
from utilities_indemnity import create_indemnity,create_indemnity_
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres
from utilities_contract import get_contract_id
from utilities_company import get_company_by_extern_id
def add_one_sinister_(id,contract_id):
 
    if request.method=='POST':
        try:
            description=request.form['description']
            opposing_insurer=request.form['opposing_insurer']
            amount=request.form['amount']
            sinister_date=request.form['sinister_date']
            if amount and amount !='':
                extern_id="sin"+time_number()
                sinister=Sinister(
                    sinister_date=sinister_date,
                    description=description,
                    opposing_insurer=opposing_insurer,
                    amount=float(amount))

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
            con_id=get_contract_id(contract_id,con,cur)
            cl_id=get_company_by_extern_id(id,con,cur)
            add_sinister_(sinister,extern_id,id,contract_id,cl_id,con_id,con,cur)
            
            flash('Listed Successfully !')
        except Exception as error:
            print(error)
        
        finally :
            if con is not None:
                cur.close()
                con.close()
      
        return redirect(url_for("client.display_company",id=id,contract_id=contract_id))
        
    return render_template("sinister/create_sinister.html",id=id,contract_id=contract_id)

def add_one_sinister(id,contract_id):
 
    if request.method=='POST':
        try:
            description=request.form['description']
            opposing_insurer=request.form['opposing_insurer']
            amount=request.form['amount']
            sinister_date=request.form['sinister_date']
            if amount and amount !='':
                extern_id="sin"+time_number()
                sinister=Sinister(
                    sinister_date=sinister_date,
                    description=description,
                    opposing_insurer=opposing_insurer,
                    amount=float(amount))

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
            con_id=get_contract_id(contract_id,con,cur)
            cl_id=get_client_by_extern_id(id,con,cur)
            add_sinister(sinister,extern_id,id,contract_id,cl_id,con_id,con,cur)
            
            flash('Listed Successfully !')
        except Exception as error:
            print(error)
        
        finally :
            if con is not None:
                cur.close()
                con.close()
      
        return redirect(url_for("client.display_client",id=id,contract_id=contract_id))
        
    return render_template("sinister/create_sinister.html",id=id,contract_id=contract_id)

def update_sinister(id,sinister_id):
    
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    sinister=sinister_to_update(id,sinister_id,con,cur)


    if request.method=='POST':
        print(request.form)
        try:
            update_dict={}
            modification={}
            description=request.form['description']
            opposing_insurer=request.form['opposing_insurer']
            amount=request.form['amount']
            status=request.form['status']
            sinister_date=request.form['sinister_date']

            if sinister_date:
                update_dict['sinister_date']=sinister_date

            if description:
                update_dict['description']=description
            if opposing_insurer:
                update_dict['opposing_insurer']=opposing_insurer
            if amount and amount!='':
                update_dict['amount']=float(amount)
            if status and status!='':
                
                update_dict['status']=status 
                if status=="Valide" or status=="Invalide":
                    update_dict['closing_date']=str(datetime.datetime.now().date())
            if update_dict=={}:
                flash('No Modification Is Made')
                return redirect(url_for("client.display_client",id=session['client_id'],contrcat_id=session['contract_id']))
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
            
            cl_id=get_client_by_extern_id(id,con,cur)
            con_id=get_contract_id(session['contract_id'],con,cur)



            if sinister.status=='Valide' or sinister.status=='Invalide' :
                flash("Can't Update Sinister Already Close")
            else:
                count=count_modification(sinister_id,con,cur)
                if count<=5:

                    count=count_modification(sinister_id,con,cur)
                    update_one_sinister(update_dict,id,sinister_id,con,cur)
                    
                    modification['updated_id']=sinister_id
                    modification['updates_values']=json.dumps(update_dict)
                    modification['updated_by']=session['user']
                    
                    modification['extern_id']='mdf'+time_number()
                    add_modification(modification,con,cur)
                else:
                    flash('Nombre maximale  de modification est dépassé')
                    return redirect(url_for("client.display_client",id=session['client_id'],contract_id=session['contract_id']))
                
                    

                if 'status' in update_dict.keys():
                    if update_dict['status']=='Valide':
                        if 'amount' in update_dict.keys():
                            sinister.amount=update_dict['amount']
                        extern_id="ind"+time_number()
                        create_indemnity(sinister,extern_id,cl_id,con_id,id,session['contract_id'],con,cur)
                
                flash('Updated Sucessfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_client",id=session['client_id'],contract_id=session['contract_id']))

    return render_template("sinister/modify_sinister.html",id=id,sinister_id=sinister_id,sinister=sinister)



def update_sinister_(id,sinister_id):
    
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()
    sinister=sinister_to_update(id,sinister_id,con,cur)


    if request.method=='POST':
        print(request.form)
        try:
            update_dict={}
            modification={}
            description=request.form['description']
            opposing_insurer=request.form['opposing_insurer']
            amount=request.form['amount']
            status=request.form['status']
            sinister_date=request.form['sinister_date']

            if sinister_date:
                update_dict['sinister_date']=sinister_date

            if description:
                update_dict['description']=description
            if opposing_insurer:
                update_dict['opposing_insurer']=opposing_insurer
            if amount and amount!='':
                update_dict['amount']=float(amount)
            if status and status!='':
                
                update_dict['status']=status 
                if status=="Valide" or status=="Invalide":
                    update_dict['closing_date']=str(datetime.datetime.now().date())
            if update_dict=={}:
                flash('No Modification Is Made')
                return redirect(url_for("client.display_company",id=session['client_id'],contrcat_id=session['contract_id']))
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
            
            cl_id=get_company_by_extern_id(id,con,cur)
            con_id=get_contract_id(session['contract_id'],con,cur)



            if sinister.status=='Valide' or sinister.status=='Invalide' :
                flash("Can't Update Sinister Already Close")
            else:
                count=count_modification(sinister_id,con,cur)
                if count<=5:

                    count=count_modification(sinister_id,con,cur)
                    update_one_sinister(update_dict,id,sinister_id,con,cur)
                    
                    modification['updated_id']=sinister_id
                    modification['updates_values']=json.dumps(update_dict)
                    modification['updated_by']=session['user']
                    
                    modification['extern_id']='mdf'+time_number()
                    add_modification(modification,con,cur)
                else:
                    flash('Nombre maximale  de modification est dépassé')
                    return redirect(url_for("client.display_company",id=session['client_id'],contract_id=session['contract_id']))
                
                    

                if 'status' in update_dict.keys():
                    if update_dict['status']=='Valide':
                        if 'amount' in update_dict.keys():
                            sinister.amount=update_dict['amount']
                        extern_id="ind"+time_number()
                        create_indemnity_(sinister,extern_id,cl_id,con_id,id,session['contract_id'],con,cur)
                
                flash('Updated Sucessfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_company",id=session['client_id'],contract_id=session['contract_id']))

    return render_template("sinister/modify_sinister.html",id=id,sinister_id=sinister_id,sinister=sinister)

def searching_sinisters():
    
    record=None
    columns_names=None
    if request.method=='POST':
    
        if request.form['submit']=='Chercher':
            try:
                search_dict={}
                
                status= request.form['status']
         
                opposing_insurer=request.form['opposing_insurer']
                amount=request.form['amount']
                client_id=request.form['client_id']
                date_type=request.form['date_type']
                daterange=request.form['daterange']
                date1=daterange[0:10].strip()
                date2=daterange[12:].strip()

                

                if status and status!='':
                    search_dict['status']=status

                if opposing_insurer and opposing_insurer!='':
                    search_dict['opposing_insurer']=opposing_insurer
                if amount and amount!='':
                    search_dict['amount']=amount            

                if client_id and client_id !='':
                    search_dict['extern_client_id']=client_id
                if daterange !='' and date_type !='':
                    search_dict[f'{date_type}']=f" between '{date1}' and '{date2}'"

                search_dict_dps=(json.dumps(search_dict))
                return redirect(url_for('sinister.search_result_',search_dict=search_dict_dps,page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
                "search/search_sinisters.html",search_result=record,columns=columns_names)



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
        
        count,page_result,columns_names,record=search_sinister(search_dict,page,cur)
        
        link_next=""
        link_previous=""
        max_pages=0
        
        if not record:
            flash('Zero Result , Please Check Your Search Criteria !')
            return redirect(url_for('sinister.search_sinisters'))
            
        else:
            file_name=f"search_sinister_result"
            csv_columns = columns_names.copy()
            csv_columns.insert(0,'id')
            csv_columns.remove('Link')
            csv_columns.append('number_results')
            all_record=search_all_sinister(search_dict,cur)
            to_csv(file_name,csv_columns,all_record)
            next_page=page+1
            previous=page-1
            results=page_result*page
            if count%page_result==0:
                max_pages=count//page_result
            else:
                max_pages=(count//page_result)+1
            
            if results>=count and page==1:
                
                link_next=url_for('sinister.search_result_',search_dict=search_dict_dps,page=1)

            elif page>1 and results>=count:
                link_next=url_for('sinister.search_result_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('sinister.search_result_',search_dict=search_dict_dps,page=next_page)
            if page==1:

                
                link_previous=url_for('sinister.search_result_',search_dict=search_dict_dps,page=1)
                
            else:
                link_previous=url_for('sinister.search_result_',search_dict=search_dict_dps,page=previous)
            
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
    
    return render_template(
        "search/search_sinisters.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)
