from utilities import postgres_connetion,to_csv
from config import *
import datetime 
from flask import request,url_for,abort,render_template,redirect,flash,json,session
from  utilities_company import get_all_company,search_fiche_client,company_to_update,update_company_info,search_company_pages,search_company_pages_export

def display_all_companies():
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()
        page= int(request.args.get('page', 1))
        
        count,page_result,columns_names,record=get_all_company(page,cur)
        
        next_page=page+1
        previous=page-1
        results=page_result*page
        max_pages=count//page_result

        
        print(page_result)
        if record:
            if count%page_result==0:
                max_pages=count//page_result
            else:
                max_pages=(count//page_result)+1
            
            if results>=count and page==1:
                link_next=url_for('client.get_all_companies',page=1)
            elif page>1 and results>=count:
                link_next=url_for('client.get_all_companies',page=page)
            else:
                link_next=url_for('client.get_all_companies',page=next_page)
            if page==1:
                link_previous=url_for('client.get_all_companies',page=1)
            else:
                link_previous=url_for('client.get_all_companies',page=previous)

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
            "company/companies.html",search_result=record,columns=columns_names,
            link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)

def display_one_company(id,contract_id):
    
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

    return render_template("company/fiche_company.html" ,
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


def update_companies_info(id):
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()   
    client=company_to_update(id,con,cur)
    if request.method== 'POST':
        error=True
        try:
            update_dict={}

            email=request.form['email']
            tel=request.form['tel']
            if email:
                update_dict['company_email']=email
            if tel:
                update_dict['company_tel']=tel
            if update_dict=={}:
                flash('no modification is made')
                return redirect(url_for("client.display_company",id=session['client_id'],contract_id=session['contract_id']))
                

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

            update_company_info(update_dict,id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_company",id=session['client_id'],contract_id=session['contract_id']))

    return render_template("company/modify_company_info.html",id=id,client=client)


def searching_company_():
    
    record=None
    columns_names=None
    if request.method=='POST':
    
        if request.form['submit']=='Chercher':
            try:
                search_dict={}
                client_reference=request.form['client_reference']
                name= request.form['first_name']
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
                    search_dict['company_name']=name

                if email and email!='':
                    search_dict['company_email']=email
                if tel and tel!='':
                    search_dict['company_tel']=tel            
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
                        "search/search_company.html",search_result=record,columns=columns_names)

                return redirect(url_for('client.get_search_company_',search_dict=json.dumps(search_dict),page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
        "search/search_company.html",search_result=record,columns=columns_names,now=str(datetime.datetime.now().date()))

def get_searching_company():
    
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
        
        count,page_result,columns_names,record=search_company_pages(search_dict,page,cur)
        print(record)
        print('999999999999999999')
        link_next=""
        link_previous=""
        max_pages=0
        if not record:
            redirect('client.search_company_')
            flash('Zero Result , Please Check Your Search Criteria !')
        else :
            file_name=f"search_result"
            csv_columns = columns_names.copy()

            csv_columns.remove('Link')
            csv_columns.append('contracts')
            csv_columns.append('number_results')
            record2=search_company_pages_export(search_dict,page,cur)
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
                
                link_next=url_for('client.get_search_company_',search_dict=search_dict_dps,page=1)
                
            elif page>1 and results>=count:
                link_next=url_for('client.get_search_company_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('client.get_search_company_',search_dict=search_dict_dps,page=next_page)
            if page==1:
                link_previous=url_for('client.get_search_company_',search_dict=search_dict_dps,page=1)
            else:
                link_previous=url_for('client.get_search_company_',search_dict=search_dict_dps,page=previous)

    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_company.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages,now=str(datetime.datetime.now().date()))