# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db


class Student(db.Model):
    __tablename__ = 'student_info'
    stu_id = db.Column(db.String(15), primary_key=True)
    credit = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    qresult = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    rec_result = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    balance = db.Column(db.DECIMAL(10,2), nullable=False, server_default=db.FetchedValue())
