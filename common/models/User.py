# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db


class User(db.Model):
    __tablename__ = 'teacher_info'
    tea_id = db.Column(db.Integer, primary_key=True)
    tea_email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    tea_name = db.Column(db.String(25), nullable=False, server_default=db.FetchedValue())
    password = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    teacher_intro = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())

