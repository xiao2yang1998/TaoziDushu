# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from app import db


class PCourse(db.Model):
    __tablename__ = 'percourse_info'
    pcourse_id = db.Column(db.Integer, primary_key=True)
    vedio_url = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    pcourse_intro = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())
    pcourse_imgurl = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    pcourse_title = db.Column(db.String(250), nullable=False, server_default=db.FetchedValue())


