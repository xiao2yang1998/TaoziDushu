# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,g,redirect,render_template,current_app
from flask import session,flash,url_for
from common.models.User import ( User )
from app import app,db,db_sql
import json
from controllers.homework import Homework

route_user = Blueprint( 'user_page',__name__  )
cursor = db_sql.cursor()


@route_user.route( "/login",methods = [ "GET","POST" ] )
def login():
    if request.method == 'POST':
        current_app.logger.debug("login post method")
        username = request.form['username']
        password = request.form['password']

        user_info = User.query.filter_by( tea_email = username ).first()
        if not user_info:
            flash('用戶名或密碼錯誤!', 'error')
            return render_template('auth-login.html')

        if user_info.password != password:
            flash('用戶名或密碼錯誤!','error')
            return  render_template('auth-login.html')
        session['username'] = username
        session['password'] = password
        session['tea_id'] = user_info.tea_id
        session['tea_name'] = user_info.tea_name
        print(session['tea_name'],session['username'])
        flash('登錄成功!', 'message')
        url = url_for("homework_page.Ckeck",tea_id = user_info.tea_id)
        return redirect(url)
    return render_template('auth-login.html')


@route_user.route( "/logout")
def logout():
    session.clear()  # 清除所有session
    return redirect("")


@route_user.route( "/admin_login",methods = [ "GET","POST" ] )
def admin_login():
    if request.method == 'POST':
        current_app.logger.debug("login post method")
        username = request.form['username']
        password = request.form['password']
        exe = 'select * from admin_info where email = \"%s\" and password = \"%s\" ' % (username,password)
        cursor.execute(exe)
        print(exe)
        re = cursor.fetchall()
        print(re)
        if re :
            re = re[0]
            session['username'] = username
            session['password'] = password
            session['admin_id'] = re[0]
            flash('登錄成功!', 'message')
            return render_template('adminMain.html')
        else:
            flash('用戶名或密碼錯誤!', 'error')
            return render_template('admin_login.html')
    return render_template('admin_login.html')




