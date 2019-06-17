#-*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import session, render_template, request, make_response
from flask import current_app
from flask import jsonify,url_for, redirect
from flask_paginate import Pagination,get_page_parameter
import pymysql


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:00000000@localhost/readingmanagement'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

#
db_sql = pymysql.connect('localhost','root','00000000','readingmanagement',charset = 'utf8')
# cursor = db2.cursor()

from controllers.user.User import route_user
from controllers.course.Course import route_course
from controllers.student.Student import route_student
from controllers.homework.Homework import route_homework
from controllers.admin.Admin import route_admin

app.register_blueprint(route_user)
app.register_blueprint(route_course)
app.register_blueprint(route_student)
app.register_blueprint(route_homework)
app.register_blueprint(route_admin)

@app.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.debug(" index page")
    current_app.logger.debug("cookie name %s" % request.cookies.get('username'))
    current_app.logger.debug('in login %s %s'%(session.keys(),session.values()))
    if 'username' in session:
        return redirect(url_for("homework_page.Ckeck",tea_id = session['username'] ))
        #logger.debug("login user is %s" % flask_login.current_user)
        #logger.debug('Logged in as %s' % escape(session['username']))
        return render_template('index.html', name=session['username'])
    else:
        current_app.logger.debug("you are not logged in")
        return render_template('auth-login.html')



if __name__ == '__main__':
    app.run()
