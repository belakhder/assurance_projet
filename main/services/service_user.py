
from flask import Flask,render_template,request,url_for,abort,jsonify,redirect,flash,session,g,json
from main.models.user import User
import uuid
from utilities import postgres_connetion,time_number,loads_settings,to_csv
from utilities_user import login,hash_string,create_user,get_all_user,search_user_pages,update_user_info,insert_settings,update_settings_info,user_to_update,search_all_user
import psycopg2
from psycopg2.errors import UniqueViolation
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def subscription():

    con=None
    if request.method=='POST':
        if request.form['submit']=="S'abonner":
            
            try :
                register_user=False
                id="usr"+time_number()
                name= request.form.get('name')
                last_name=request.form.get('last_name')
                email=request.form.get('email')
                tel=request.form.get('phone')
                user_name=request.form.get('user_name')
                password=request.form.get('password')
                user_type=request.form.get('user_type')

                user=User(
                    name=name,
                    last_name=last_name,
                    email=email,
                    tel=tel,
                    id=id,
                    user_name=user_name,
                    password=password,
                    user_type=user_type)
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
                create_user(user,con,cur)
                register_user=True
                
            except (Exception, psycopg2.Error) as error:
                print(error)
                if  isinstance(error,UniqueViolation):
                    flash('Les informations choisies existent déjà')
                else:
                    abort(422)
            finally:
                if con is not None:
                    cur.close()
                    con.close()
            if register_user==True:
                flash('Utilisateur répertorié avec succès')
    return render_template("user/subscription_user.html")

def login_user():
    
    con=None
    if request.method=='POST':
        
        if request.form['submit']=='Se connecter':
            print(session)
            session.permanen=False
            if 'user' not in session:
                
                try :
                    user_name=request.form['user_name']
                    password=request.form['password']
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
                    [check,id]=login(user_name,password,cur)
                    
                    if check==True:
                        session['user']=id
                        session['settings']=loads_settings()

                except Exception as error:
                    print(error)
                    abort(422)
                finally :
                    if con is not None:
                        cur.close()
                        con.close()
                
                if  'user' in session  :  
                   
                    return redirect(url_for('client.search_client_'))

            else:
                print(session)
                flash("Vous êtes déjà connecté")
                return redirect(url_for('client.search_client_'))
                
        
    return render_template("page_acceuil.html")



def logout():
    if 'user' not in session:
        flash('You are already louged out , please login !')
        print(session)
    else:
        session.pop('user',None)
        flash('You are louged out , please login !')
        print(session)
    return redirect(url_for('user.login_users'))

def display_all_user():
    try:
        con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
        cur=con.cursor()

        page= int(request.args.get('page', 1))
        
        count,page_result,columns_names,record=get_all_user(page,cur)
        
        next_page=page+1
        previous=page-1
        results=page_result*page
        
        max_pages=count//page_result
        if count%page_result==0:
            max_pages=count//page_result
        else:
            max_pages=(count//page_result)+1

        if results>=count and page==1:
            link_next=url_for('user.get_all_users',page=1)
        elif page>1 and results>=count:
            link_next=url_for('user.get_all_users',page=page)
        else:
            link_next=url_for('user.get_all_users',page=next_page)
        if page==1:
            link_previous=url_for('user.get_all_users',page=1)
        else:
            link_previous=url_for('user.get_all_users',page=previous)
        
    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()
        return render_template(
            "user/users.html",search_result=record,columns=columns_names,
                link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)



def searching_user_():
    
    record=None
    columns_names=None
    if request.method=='POST':
        
        if request.form['submit']=='Chercher':
            try:
                print(request.form)
                search_dict={}
                user_reference=request.form['user_reference']
                name= request.form['first_name']
                last_name=request.form['last_name']
                email=request.form['email']
                tel=request.form['tel']
                user_type=request.form['user_type']
                

                if user_reference and user_reference!='':
                    search_dict['id']=user_reference
                if name and name!='':
                    search_dict['name']=name
                if last_name and last_name!='':
                    search_dict['last_name']=last_name
                if email and email!='':
                    search_dict['email']=email
                if tel and tel!='':
                    search_dict['tel']=tel            

                if user_type and user_type !='':
                    search_dict['user_type']=user_type
                print(search_dict)
                if search_dict=={}:
                    flash('Please Enter At Least One Field')
                    return render_template(
                        "search/search_user.html",search_result=record,columns=columns_names)
                    
                
                
                return redirect(url_for('user.get_search_user_',search_dict=json.dumps(search_dict),page=1))
            except Exception as error:
                print(error)
                abort(400)
    return render_template(
        "search/search_user.html",search_result=record,columns=columns_names)

def get_searching_user():
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

        count,page_result,columns_names,record=search_user_pages(search_dict,page,cur)
        link_next=""
        link_previous=""
        max_pages=0
        if not record:
            redirect('user.search_user_')
            flash("Zéro Résultat , Merci D'affiner votre recherche !")
        else :
            file_name=f"search_user_result"
            csv_columns = columns_names.copy()
            csv_columns.insert(0,'id')
            csv_columns.remove('Link')
            csv_columns.append('nombre de resultat')
            all_record=search_all_user(search_dict,cur)
            to_csv(file_name,csv_columns,all_record)
            next_page=page+1
            previous=page-1
            results=page_result*page
            
            if count%page_result==0:
                max_pages=count//page_result
            else:
                max_pages=count//page_result
                max_pages=max_pages+1

            if results>=count and page==1:
                
                link_next=url_for('user.get_search_user_',search_dict=search_dict_dps,page=1)
                
            elif page>1 and results>=count:
                link_next=url_for('user.get_search_user_',search_dict=search_dict_dps,page=page)
            else:
                link_next=url_for('user.get_search_user_',search_dict=search_dict_dps,page=next_page)
            if page==1:
                link_previous=url_for('user.get_search_user_',search_dict=search_dict_dps,page=1)
            else:
                link_previous=url_for('user.get_search_user_',search_dict=search_dict_dps,page=previous)

    except Exception as error:
        print(error)
        abort(422)
    finally :
        if con is not None:
            cur.close()
            con.close()

    return render_template(
        "search/search_user.html",search_result=record,columns=columns_names,
            search_dict=search_dict_dps,link_next=link_next,link_previous=link_previous,page=page,nb=page_result,max_pages=max_pages)


def update_users_info(id):
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor() 
    user=user_to_update(id,con,cur)
    if request.method== 'POST':
        error=True
        try:
            update_dict={}
            name= request.form.get('name')
            last_name=request.form.get('last_name')
            email=request.form.get('email')
            tel=request.form.get('tel')
            user_name=request.form.get('user_name')
            password=request.form.get('password')
            user_type=request.form.get('user_type')
            if name:
                update_dict['name']=name
            if last_name:
                update_dict['last_name']=last_name
            if email:
                update_dict['email']=email
            if tel:
                update_dict['tel']=tel
            if user_name:
                update_dict['user_name']=user_name   
            if password:
                update_dict['password']=password
            if user_type:
                update_dict['user_type']=user_type                                                 
            if update_dict=={}:
                flash('no modification is made')
                return redirect(url_for("user.get_all_users"))
                

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

            update_user_info(update_dict,id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("user.get_all_users"))

    return render_template("user/modify_user_info.html",id=id,user=user)

def insert_settings_():
    con=None
    if request.method=='POST':
        print(request.form)
        if request.form['submit']=="Valider":
            try :
                step= request.form.get('step')
                max_inst=request.form.get('max_inst')
                keys='step,max_inst'
                values=(step,max_inst)

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
                insert_settings(keys,values,con,cur)
                flash('paramétres enregistrés')
                
            except Exception as error:
                print(error)
                abort(422)
            finally :
                if con is not None:
                    cur.close()
                    con.close()
    return render_template('settings.html')

def update_settings():
    
    if request.method== 'POST':
        error=True
        try:
            update_dict={}
            step= request.form.get('step')
            max_inst=request.form.get('max_inst')
            
            if step:
                update_dict['step']=step
            if max_inst:
                update_dict['max_inst']=max_inst
                            
            if update_dict=={}:
                flash('no modification is made')
                
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

            update_settings_info(update_dict,'1',con,cur)
            session['settings']=(step,max_inst)
            print(session)
            flash('Updated Successfully !')
            
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        

    return  render_template('modify_settings.html')