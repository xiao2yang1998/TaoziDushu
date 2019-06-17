# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,g,redirect,render_template,current_app
from flask import session,url_for
from common.models.User import ( User )
from common.models.Course import ( Course )
from common.models.Student import ( Student )
from common.models.Homework import ( Homework )
from common.models.Problem import (Problem)
from app import app,db,db_sql
import os
import json


route_homework = Blueprint( 'homework_page',__name__  )
cursor = db_sql.cursor()


@route_homework.route( "/homework/<homework_id>",methods = [ "GET","POST" ] )
def ShowHomework(homework_id):
    homework_info = Homework.query.filter_by(homework_id=homework_id).first()
    problem_info = Problem.query.filter_by(pcourse_id=homework_info.pcourse_id).all()
    print(homework_info,problem_info)
    return render_template("correction.html",homework_info=homework_info,problem_info=problem_info)


@route_homework.route( "/admin_homework/<homework_id>",methods = [ "GET","POST" ] )
def admin_ShowHomework(homework_id):
    homework_info = Homework.query.filter_by(homework_id=homework_id).first()
    problem_info = Problem.query.filter_by(pcourse_id=homework_info.pcourse_id).all()
    print(homework_info, problem_info)
    return render_template("admin_correction.html", homework_info=homework_info, problem_info=problem_info)


@route_homework.route( "/homework/Comment/<homework_id>",methods = [ "GET","POST" ] )
def SubmitComment(homework_id):
    homework_info = Homework.query.filter_by(homework_id=homework_id).first()
    homework_info.done = 2
    print(request.form)
    homework_info.comment = request.form['comment']
    db_sql.commit()
    return render_template("index.html")

@route_homework.route( "/homework/ckeck/<tea_id>",methods = [ "GET","POST" ] )
def Ckeck(tea_id):
    tea_id = session['tea_id']
    print(tea_id,type(tea_id))
    exe = "select class_id,scourse_id from class_info where tea_id = %d" %(tea_id)
    cursor.execute(exe)
    print(exe)
    class_setcourse_data = cursor.fetchall()
    print(class_setcourse_data)
    class_setcourse_title_data = []
    for p in class_setcourse_data:
        p = list(p)

        scourse_info = Course.query.filter_by( scourse_id = p[1] ).first()
        temp = scourse_info.scourse_title

        exe = "select (f_getclass_student_num(%d))"%p[0]
        cursor.execute(exe)
        sum = cursor.fetchone()
        sum = sum[0]
        p.append(temp)
        p.append(str(sum))
        class_setcourse_title_data.append(p)

    print(class_setcourse_title_data)

    resp = make_response(render_template('index.html', class_setcourse_title = class_setcourse_title_data))
    return resp


@route_homework.route( "/stu_homework/<homework_id>",methods = [ "GET","POST" ] )
def stu_ShowHomework(homework_id):
    homework_info = Homework.query.filter_by(homework_id=homework_id).first()
    problem_info = Problem.query.filter_by(pcourse_id=homework_info.pcourse_id).all()
    print(homework_info,problem_info)
    return render_template("finish.html",homework_info=homework_info,problem_info=problem_info)

@route_homework.route( "/homework/stu_finish/<homework_id>",methods = [ "GET","POST" ] )
def SubmitAns(homework_id):
    homework_info = Homework.query.filter_by(homework_id=homework_id).first()
    homework_info.done = 1
    file = request.files.get("files")
    path_static = "F:/test.v0/static/img"
    imgurl ='homework'+ str(homework_id) + '.jpg'
    homework_info.store_url = imgurl
    up_path = os.path.join(path_static, imgurl)
    file.save(up_path)
    db_sql.commit()
    url = url_for("student_page.showinfo")
    return redirect(url)



