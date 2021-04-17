
from flask import Flask,render_template,request,url_for,abort,jsonify,redirect,flash,session,json,make_response
import datetime
from utilities import postgres_connetion,time_number,to_csv,money_contract,money_instalment,money_payment,money_indemnity,money_sinister,add_months



def moneys_contract():
    record=money_contract(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record2=money_instalment(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record3=money_payment(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record4=money_indemnity(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    record5=money_sinister(add_months(datetime.datetime.now().date(),-1),str(datetime.datetime.now().date()))
    date1=add_months(datetime.datetime.now().date(),-1).strftime("%d-%m-%Y")
    date2=(datetime.datetime.now().date()).strftime("%d-%m-%Y")
    date={}
    if request.method=='POST':
        print(request.form)
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

    return render_template(
        'dashbord/dashbord_contract.html',
        record=record,
        record2=record2,
        record3=record3,
        record4=record4,
        record5=record5,
        date1=date1,
        date2=date2,
        date=date)

