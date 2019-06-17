# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db


class Homework(db.Model):
    __tablename__ = 'homework_info'
    homework_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    stu_id = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue())
    pcourse_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    done = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    comment = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())
    store_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())

