# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,g,redirect,render_template,current_app
from flask import session,flash,url_for
from common.models.User import ( User )
from common.models.Course import ( Course )
from common.models.Student import ( Student )
from common.models.Problem import (Problem)
from common.models.PCourse import (PCourse)
from flask_paginate import Pagination,get_page_parameter
from app import app,db,db_sql
import json


route_student = Blueprint( 'student_page',__name__  )
cursor = db_sql.cursor()

@route_student.route( "/student",methods = [ "GET","POST" ] )
def ShowStudents():
    tea_id = session['tea_id']
    exe = '''
      select stu_id,class_id from inclass where class_id in 
     (select class_id from class_info where tea_id = %d)''' % tea_id
    cursor.execute(exe)
    stu_class_data = cursor.fetchall()
    current_app.logger.debug(stu_class_data)
    resp = make_response(render_template('student.html', student_class=stu_class_data))
    return resp


@route_student.route( "/student/<stu_id>",methods = [ "GET","POST" ] )
def ShowStudentInfo(stu_id):
    stu_info = Student.query.filter_by(stu_id = stu_id).first()
    exe = 'select class_id from inclass where stu_id = \"%s\"' % stu_id
    cursor.execute(exe)
    all_class_id = cursor.fetchall()
    class_homework_data = {}
    for class_id in all_class_id:
        class_id = class_id[0]
        exe = "select scourse_id from class_info where class_id =%d " %class_id
        cursor.execute(exe)
        scourse_id = cursor.fetchone()
        scourse_id = scourse_id[0]
        exe = 'select scourse_id,homework_id,done,thenumber from homework_info natural join s_p_class_info where stu_id=\"%s\" and class_id = \"%s\" and scourse_id=\"%s\" order by thenumber' % (
        stu_info.stu_id, class_id,scourse_id)
        cursor.execute(exe)
        homework_data = cursor.fetchall()
        print(exe)
        class_homework_data[class_id] = homework_data
    # 去除鍵值對為空的pair
    for key in list(class_homework_data.keys()):
        if not class_homework_data.get(key):
            del class_homework_data[key]
    resp = make_response(render_template('onestu.html', student= stu_info,class_homework=class_homework_data))
    return resp

@route_student.route( "/admin_student/<stu_id>",methods = [ "GET","POST" ] )
def admin_show_student_info(stu_id):
    stu_info = Student.query.filter_by(stu_id = stu_id).first()
    exe = 'select class_id from inclass where stu_id = \"%s\"' % stu_id
    cursor.execute(exe)
    all_class_id = cursor.fetchall()
    class_homework_data = {}
    for class_id in all_class_id:
        class_id = class_id[0]
        exe = "select scourse_id from class_info where class_id = " + "class_id"
        cursor.execute(exe)
        scourse_id = cursor.fetchone()
        scourse_id = scourse_id[0]
        exe = 'select scourse_id,homework_id,done,thenumber from total_homework_info where stu_id=\"%s\" and class_id = \"%s\" order by thenumber' % (
        stu_info.stu_id, class_id)
        cursor.execute(exe)
        homework_data = cursor.fetchall()
        print(exe)
        class_homework_data[class_id] = homework_data
    # 去除鍵值對為空的pair
    for key in list(class_homework_data.keys()):
        if not class_homework_data.get(key):
            del class_homework_data[key]
    resp = make_response(render_template('admin_onestu.html', student= stu_info,class_homework=class_homework_data))
    return resp


@route_student.route( "/student_login" )
def student_login():
    return render_template("student_login.html")


@route_student.route("/student_login_check",methods = [ "POST" ] )
def student_login_check():
    if request.method == 'POST':
        print(request.form)
        stu_id = request.form['stu_id']
        student_info = Student.query.filter_by(stu_id=stu_id).first()
        if not student_info:
            flash('学生账户不存在!', 'error')
            return render_template("student_login.html")

        session['stu_id'] = stu_id
        print(stu_id)
        url = url_for("student_page.showinfo")
        return redirect(url)


@route_student.route("/student_index")
def showinfo():
    stu_id = session['stu_id']
    stu_info = Student.query.filter_by(stu_id=stu_id).first()
    exe = 'select class_id from inclass where stu_id = \"%s\"' % stu_id
    cursor.execute(exe)
    all_class_id = cursor.fetchall()
    class_homework_data = {}
    for class_id in all_class_id:
        class_id = class_id[0]
        exe = "select scourse_id from class_info where class_id =%d " % class_id
        cursor.execute(exe)
        scourse_id = cursor.fetchone()
        scourse_id = scourse_id[0]
        exe = 'select scourse_id,homework_id,done,thenumber from homework_info natural join s_p_class_info where stu_id=\"%s\" and class_id = \"%s\" and scourse_id=\"%s\" order by thenumber' % (
            stu_info.stu_id, class_id, scourse_id)
        cursor.execute(exe)
        homework_data = cursor.fetchall()
        print(exe)
        class_homework_data[class_id] = homework_data
    # 去除鍵值對為空的pair
    for key in list(class_homework_data.keys()):
        if not class_homework_data.get(key):
            del class_homework_data[key]
    resp = make_response(render_template('student_index.html', student=stu_info, class_homework=class_homework_data))
    return resp

@route_student.route("/student_show_course")
def show_course():
    stu_id = session['stu_id']
    sql = 'select * from stu_class_tea_course order by class_id'
    cursor.execute(sql)
    re = cursor.fetchall()
    sql = "select class_id from inclass where stu_id='%s'"%stu_id
    cursor.execute(sql)
    joined_class = cursor.fetchall()
    joined_class = [i[0] for i in joined_class]
    return render_template("stu_showCourse.html", classes=re,joined_class=joined_class)


@route_student.route("/student_join_class/<class_id>",methods = [ "GET","POST" ])
def join_calss(class_id):
    stu_id = session['stu_id']
    sql = "select(f_get_balance('%s'))"%stu_id
    print(sql)
    cursor.execute(sql)
    re = cursor.fetchall()
    stu_balance = re[0][0]

    sql = "select scourse_price from stu_class_tea_course where class_id=%d" % int(class_id)
    print(sql)
    cursor.execute(sql)
    re = cursor.fetchall()
    price = float(re[0][0])

    if stu_balance < price:
        return render_template("recharge.html",stu_balance = stu_balance)
    sql = "call p_join_class(%s,%d)"%(stu_id,int(class_id))
    cursor.execute(sql)
    db_sql.commit()
    url = url_for("student_page.showinfo")
    return redirect(url)

@route_student.route("/to_recharge/<stu_balance>",methods = [ "GET","POST" ])
def to_recharge(stu_balance):
    return render_template("recharge.html", stu_balance=stu_balance)

@route_student.route("/recharge",methods = [ "GET","POST" ])
def recharge():
    stu_id = session['stu_id']
    money = request.form['money']
    sql = "call p_stu_recharge('%s',%d)"%(stu_id,int(money))
    cursor.execute(sql)
    db_sql.commit()
    url = url_for("student_page.show_course")
    return redirect(url)

@route_student.route("/reading",methods = [ "GET","POST" ])
def show_book():
    stu_id = session['stu_id']
    PER_PAGE = 10
    total = PCourse.query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    pagination = Pagination(bs_version=3, page=page, total=total)
    percourses = PCourse.query.slice(start, end)
    sql = "select pcourse_id from stu_read where stu_id='%s'"%stu_id
    cursor.execute(sql)
    re = cursor.fetchall()
    read = [ i[0] for i in re]
    context = {
        'pagination': pagination,
        'percourses': percourses,
        'read':read
    }
    return render_template('stu_reading.html', **context)


@route_student.route("/read_book/<pcourse_id>",methods = [ "GET","POST" ])
def to_read(pcourse_id):
    pcourse = PCourse.query.filter_by(pcourse_id = pcourse_id).first()
    print(pcourse)
    return render_template("readingbook.html",pcourse=pcourse)

@route_student.route("/buy_book/<pcourse_id>",methods = [ "GET","POST" ])
def to_buy_pcourse(pcourse_id):
    stu_id = session['stu_id']
    sql = "select(f_get_balance('%s'))" % stu_id
    cursor.execute(sql)
    re = cursor.fetchall()
    stu_balance = re[0][0]

    if stu_balance < 1:
        return render_template("recharge.html", stu_balance=stu_balance)
    sql = "call p_read_percouse(%s,%d)" % (stu_id, int(pcourse_id))
    cursor.execute(sql)
    db_sql.commit()
    url = url_for("student_page.to_read",pcourse_id=pcourse_id)
    return redirect(url)

@route_student.route( "/stu_logout")
def logout():
    session.clear()  # 清除所有session
    url = url_for("student_page.student_login")
    return redirect(url)
