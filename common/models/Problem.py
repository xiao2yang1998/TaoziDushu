# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db


class Problem(db.Model):
    __tablename__ = 'problems'
    pro_id = db.Column(db.Integer, primary_key=True)
    pro_stem = db.Column(db.Text, nullable=False, server_default=db.FetchedValue())
    choice = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    answer = db.Column(db.CHAR, nullable=False, server_default=db.FetchedValue())
    flag = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pcourse_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pro_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

