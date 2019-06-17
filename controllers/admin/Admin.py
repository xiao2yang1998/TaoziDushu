# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify,make_response,g,redirect,render_template,current_app
from flask import session,flash,url_for
from common.models.User import ( User )
from common.models.PCourse import (PCourse)
from common.models.Course import (Course)
from common.models.Problem import (Problem)
from app import app,db,db_sql
from flask_paginate import Pagination,get_page_parameter
import json
import os
from controllers.homework import Homework


route_admin = Blueprint( 'admin_page',__name__  )
cursor = db_sql.cursor()


@route_admin.route( "/manageTeacher",methods = [ "GET","POST" ] )
def ShowAllTeachers():
    exe = "select * from teacher_info"
    cursor.execute(exe)
    teachers_data = cursor.fetchall()
    resp = make_response(render_template('manageTeacher.html', teachers=teachers_data))
    return resp

@route_admin.route( "/toaddTeacher",methods = [ "GET","POST" ] )
def toAddTeacher():
    return render_template("addTeacher.html")

@route_admin.route( "/todelTeacher/<tea_id>",methods = [ "GET","POST" ] )
def toDelTeacher(tea_id):
    tea_id = int(tea_id)
    exe = "delete from teacher_info where tea_id = %d"%tea_id
    cursor.execute(exe)
    db_sql.commit()
    url = url_for("admin_page.ShowAllTeachers")
    return redirect(url)

@route_admin.route("/tomodTeacher/<tea_id>", methods=["GET", "POST"])
def toModTeacher(tea_id):
    user_info = User.query.filter_by(tea_id=tea_id).first()
    print(user_info)
    return render_template("admin_modTeacher.html",user = user_info)


@route_admin.route("/modTeacher/<tea_id>", methods=["GET", "POST"])
def modTeacher(tea_id):
    tea_id = int(tea_id)
    if request.method == 'POST':
        print(request.form)
        tea_name = request.form['tea_name']
        print(tea_name)
        tea_email = request.form['tea_email']
        password = request.form['password']
        teacher_intro = request.form['teacher_intro']
        print(tea_name,tea_email,teacher_intro,password)
        exe = "call p_mod_teacher(%d,'%s','%s','%s','%s')"%(tea_id,tea_name,tea_email,password,teacher_intro)
        cursor.execute(exe)
        db_sql.commit()
        url = url_for("admin_page.ShowAllTeachers")
        return redirect(url)


@route_admin.route( "/addTeacher",methods = [ "GET","POST" ] )
def addTeacher():
    print(request.method)
    if request.method == 'POST':
        print(request.form)
        tea_name = request.form['tea_name']
        print(tea_name)
        tea_email = request.form['tea_email']
        password = request.form['password']
        teacher_intro = request.form['teacher_intro']
        print(tea_name,tea_email,teacher_intro,password)
        exe = "call p_add_teacher('%s','%s','%s','%s')"%(tea_name,tea_email,password,teacher_intro)
        cursor.execute(exe)
        db_sql.commit()
        url = url_for("admin_page.ShowAllTeachers")
        return redirect(url)
    return render_template("manageTeacher.html")


@route_admin.route( "/manageStudent",methods = [ "GET","POST" ] )
def ShowAllStudents():
    exe = "select * from student_info"
    cursor.execute(exe)
    students_data = cursor.fetchall()
    resp = make_response(render_template('manageStudent.html', students = students_data))
    return resp


@route_admin.route( "/manageCourse")
def show_courses():
    setcourses = Course.query.all()
    print(setcourses)

    context = {
        'setcourses':setcourses
    }
    return render_template('manageCourse.html',**context)


@route_admin.route( "/managePcourse")
def show_pcourses():
    PER_PAGE = 10
    total = PCourse.query.count()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=3,page=page,total=total)
    percourses = PCourse.query.slice(start,end)
    context = {
        'pagination':pagination,
        'percourses':percourses,
    }
    return render_template('managePcourse.html',**context)


@route_admin.route( "/toAddPcourse")
def to_add_pcourse():
    return render_template("addPcourse.html")


@route_admin.route( "/addPcourse",methods = [ "GET","POST" ] )
def add_pcourse():
    if request.method == "POST":
        try:
            file = request.files.get("files")
        except:
            print("没传文件")
        pcourse_title = request.form['pcourse_title']
        pcourse_intro = request.form['pcourse_intro']
        exe = "insert into percourse_info(pcourse_title,pcourse_intro) values('%s','%s')"%(pcourse_title,pcourse_intro)
        cursor.execute(exe)
        db_sql.commit()
        pcourse_info = PCourse.query.filter_by(pcourse_title=pcourse_title).first()

        # 写的绝对路径，可自己修改
        path_static = "F:/test.v0/static/img"
        imgurl = str(pcourse_info.pcourse_id)+'.jpg'
        up_path = os.path.join(path_static,imgurl )
        # 文件保存
        file.save(up_path)
        sql = "update percourse_info set pcourse_imgurl='%s' where pcourse_id=%d"%(imgurl,pcourse_info.pcourse_id)
        cursor.execute(sql)
        db_sql.commit()


        for i in range(1,4):
            print(request.form)
            pro_stem = request.form['pro_stem'+str(i)]
            pro_num = i
            flag = request.form['flag'+str(i)]
            flag = int(flag)
            exe = "insert into problems(pro_stem,flag,pcourse_id,pro_num) values('%s',%d,%d,%d)"%(pro_stem,flag,pcourse_info.pcourse_id,i)
            if(flag ==0 ):
                choice = request.form['choice'+str(i)]
                answer = request.form['ans'+str(i)]
                exe = "insert into problems(pro_stem,flag,pcourse_id,pro_num,choice,answer) values('%s',%d,%d,%d,'%s','%s')" % (pro_stem, flag, pcourse_info.pcourse_id, i,choice,answer)
            cursor.execute(exe)
            db_sql.commit()
            url = url_for("admin_page.show_pcourses")
            return redirect(url)


@route_admin.route( "/tomodPcourse/<pcourse_id>",methods = [ "GET","POST" ] )
def to_show_pcourse(pcourse_id):
    pcourse_info = PCourse.query.filter_by(pcourse_id=pcourse_id).first()
    exe = 'select(f_get_pcourse_problem(%d))'%pcourse_info.pcourse_id
    cursor.execute(exe)
    re = cursor.fetchall()
    re = re[0][0]
    re = re[:-1]
    re = re.split(',')
    num = len(re)
    problems = []
    if num==1:
        if re[0]=='':
            num = 0
            return render_template("admin_modPcourse.html", num=num, pcourse_info=pcourse_info, problems=problems)
    re = [ int(i) for i in re]
    for i in re:
        problem_info = Problem.query.filter_by(pro_id = i).first()
        problems.append(problem_info)
    for i in range(num):
        print(problems[i].pro_stem)
    print(problems)
    return render_template("admin_modPcourse.html",num=num,pcourse_info=pcourse_info,problems=problems)


@route_admin.route( "/modPcourse/<pcourse_id>",methods = ["GET","POST" ] )
def mod_pcourse(pcourse_id):
    if request.method == "POST":
        update_page_img = 0
        print(request.form)

        file = request.files.get("files")
        if file.filename:
            update_page_img = 1

        pcourse_id = request.form['pcourse_id']
        pcourse_title = request.form['pcourse_title']
        pcourse_intro = request.form['pcourse_intro']
        pcourse_info = PCourse.query.filter_by(pcourse_id=pcourse_id).first()
        if update_page_img == 1:
            # 写的绝对路径，可自己修改
            path_static = "F:/test.v0/static/img"
            imgurl = str(pcourse_info.pcourse_id)+'.jpg'
            up_path = os.path.join(path_static,imgurl )
            # 文件保存
            file.save(up_path)
            sql = "update percourse_info set pcourse_imgurl='%s' where pcourse_id=%d"%(imgurl,pcourse_id)
            cursor.execute(sql)
            db_sql.commit()

        sql = "call p_mod_pcourse(%d,'%s','%s')"%(pcourse_info.pcourse_id,pcourse_title,pcourse_intro)
        cursor.execute(sql)
        db_sql.commit()

        url = url_for("admin_page.show_pcourses")
        return redirect(url)

@route_admin.route( "/addCourse")
def to_add_course():
    pcourse = PCourse.query.all()
    return  render_template("addCourse.html",pcourse=pcourse)


@route_admin.route( "/wahtaddcourse",methods = [ "GET","POST" ] )
def add_course():
    if request.method == "POST":
        print(request.form)
        scourse_title = request.form['scourse_title']
        scourse_theme = request.form['scourse_theme']
        scourse_stage = request.form['scourse_stage']
        scourse_intro = request.form['scourse_intro']
        scourse_credit = request.form['scourse_credit']
        scourse_price = request.form['scourse_price']
        scourse_theme = 'theme'+scourse_theme
        scourse_stage = 'stage'+scourse_stage
        if scourse_credit!='':
            scourse_credit = int(scourse_credit)
        else :
            scourse_credit=0
        if scourse_price!='':
           scourse_price = float(scourse_price)
        else:
            scourse_price = 0
        print(scourse_credit,scourse_price)

        sql = " insert into setcourse_info(scourse_title,scourse_theme,scourse_stage,scourse_intro,scourse_credit,scourse_price)" \
              "values('%s','%s','%s','%s',%d,%f)"%(scourse_title,scourse_theme,scourse_stage,scourse_intro,scourse_credit,scourse_price)
        cursor.execute(sql)
        db_sql.commit()
        print(sql)

        scourse_info = Course.query.filter_by(scourse_title=scourse_title).first()
        pcourse1 = request.form['pcourse1']
        pcourse2 = request.form['pcourse2']
        pcourse3 = request.form['pcourse3']
        pcourse_id = [pcourse1,pcourse2,pcourse3]
        temp = []
        for i in pcourse_id:
            print(i)
            if i not in temp:
                temp.append(int(i))
        pcourse_id = temp
        for i in pcourse_id:
            sql = "call p_add_pcourse2scourse(%d,%d)"%(scourse_info.scourse_id,i)
            cursor.execute(sql)
            db_sql.commit()
    url = url_for("admin_page.show_courses")
    return redirect(url)


@route_admin.route( "/tomodcourse/<scourse_id>",methods = [ "GET","POST" ] )
def to_mod_course(scourse_id):
    scourse_info = Course.query.filter_by(scourse_id=scourse_id).first()
    sql = 'select(f_able_to_mod_scourse(%d))'%int(scourse_id)
    cursor.execute(sql)
    re = cursor.fetchall()
    re = re[0][0]
    able = 0
    if re==0:
        able=1;
    pcourses =[]
    sql = "select(f_get_scourse_pcourse(%d))"%scourse_info.scourse_id
    cursor.execute(sql)
    re = cursor.fetchall()
    re = re[0][0]
    re = re[:-1]
    re = re.split(',')
    num = len(re)
    pcourse = PCourse.query.all()
    if num == 1:
        if re[0] == '':
            num = 0
            return render_template("admin_modCourse.html",scourse = scourse_info, num=num, pcourse=pcourse,able=able)
    re = [int(i) for i in re]

    return  render_template("admin_modCourse.html",scourse = scourse_info,num=num,pcourse = pcourse,able=able,re = re)


@route_admin.route( "/showClasses")
def show_classes():
    sql = 'select * from class_tea_course order by class_id'
    cursor.execute(sql)
    re = cursor.fetchall()
    return  render_template("manageClass.html",classes = re)


@route_admin.route( "/toAddClass")
def to_add_class():
    sql = 'select * from teacher_info '
    cursor.execute(sql)
    teacher = cursor.fetchall()
    course = Course.query.all()
    return  render_template("addClass.html",teacher=teacher,course=course)

@route_admin.route( "/AddClass",methods = [ "GET","POST" ])
def add_class():
    if request.method=='POST':
        print(request.form)
        tea_id = request.form['teacher_id']
        scourse_id = request.form['scourse_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        tea_id = int(tea_id)
        scourse_id = int(scourse_id)
        sql = "call p_add_class(%d,%d,'%s','%s')"%(tea_id,scourse_id,start_time,end_time)
        print(sql)
        cursor.execute(sql)
        db_sql.commit()
    url = url_for("admin_page.show_classes")
    return redirect(url)

@route_admin.route( "/DelClass/<class_id>",methods = [ "GET","POST" ])
def del_calss(class_id):
    sql = "delete from class_info where class_id=%d"%int(class_id)
    cursor.execute(sql)
    db_sql.commit()
    url = url_for("admin_page.show_classes")
    return redirect(url)