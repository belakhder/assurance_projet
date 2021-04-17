from flask import render_template,request,url_for,abort,redirect,flash,session
import uuid
import datetime 
from utilities_address import update_one_address,address_to_update
from utilities import postgres_connetion
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres

def update_address(id,address_id):
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()     
    address=address_to_update(id,con,cur)
    if request.method=='POST':
        try:
            update_dict={}
            line1=request.form['line1']
            line2=request.form['line2']
            city=request.form['city']
            postal_code=request.form['postal_code']
            country=request.form['country']
            state=request.form['state']

            if line1:
                update_dict['line1']=line1
            if line2:
                update_dict['line2']=line2
            if city:
                update_dict['city']=city
            if postal_code:
                update_dict['postal_code']=postal_code 
            if country:
                update_dict['country']=country
            if state:
                update_dict['state']=state
            if  update_dict=={}:
                flash('no modification is made')
                return redirect(url_for("client.display_client",id=session['client_id'],contract_id=session['contract_id']))
        except Exception as error:
            print(error)
            abort(400)
        

        if update_dict=={}:
            abort(400)

        try:
            con=postgres_connetion(
                host_postgres,
                db_name_postgres,
                db_user_postgres,
                db_password_postgres)
            cur=con.cursor()      

            update_one_address(update_dict,id,address_id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_client",id=session['client_id'],contract_id=session['contract_id']))

    return render_template("modify_client_address.html",id=id,address_id=address_id,address=address)


def update_address_(id,address_id):
    con=postgres_connetion(
        host_postgres,
        db_name_postgres,
        db_user_postgres,
        db_password_postgres)
    cur=con.cursor()     
    address=address_to_update(id,con,cur)
    if request.method=='POST':
        try:
            update_dict={}
            line1=request.form['line1']
            line2=request.form['line2']
            city=request.form['city']
            postal_code=request.form['postal_code']
            country=request.form['country']
            state=request.form['state']

            if line1:
                update_dict['line1']=line1
            if line2:
                update_dict['line2']=line2
            if city:
                update_dict['city']=city
            if postal_code:
                update_dict['postal_code']=postal_code 
            if country:
                update_dict['country']=country
            if state:
                update_dict['state']=state
            if  update_dict=={}:
                flash('no modification is made')
                return redirect(url_for("client.display_company",id=session['client_id'],contract_id=session['contract_id']))
        except Exception as error:
            print(error)
            abort(400)
        

        if update_dict=={}:
            abort(400)

        try:
            con=postgres_connetion(
                host_postgres,
                db_name_postgres,
                db_user_postgres,
                db_password_postgres)
            cur=con.cursor()      

            update_one_address(update_dict,id,address_id,con,cur)
            flash('Updated Successfully !')
        except Exception as error:
            print(error)
            abort(422)
        finally :
            if con is not None:
                cur.close()
                con.close()
        return redirect(url_for("client.display_company",id=session['client_id'],contract_id=session['contract_id']))

    return render_template("modify_client_address.html",id=id,address_id=address_id,address=address)