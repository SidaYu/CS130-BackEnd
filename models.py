from flask_sqlalchemy import SQLAlchemy
from app import db

# Todo: real model;
# user register info.
class User(db.Model):
    __tablename__ = "user_info"
    email = db.Column('email', db.String, primary_key=True)
    password = db.Column('password', db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password


# job info.
class Job(db.Model):
    __tablename__ = "job_info"
    id = db.Column('id', db.Integer, primary_key=True)
    user_email = db.Column('user_email', db.String)
    company_name = db.Column("company_name", db.String)
    company_depart = db.Column("company_depart", db.String)
    position_title = db.Column("position_title", db.String)
    app_URL = db.Column("app_URL", db.String)

    def __init__(self, user_email, company_name, company_depart, position_title, app_URL):
        self.user_email = user_email
        self.company_name = company_name
        self.company_depart = company_depart
        self.position_title = position_title
        self.app_URL = app_URL


class Job_Comment(db.Model):
    __tablename__ = "job_comment"
    id = db.Column('id', db.Integer, primary_key=True)
    job_id = db.Column('job_id', db.Integer)
    comment = db.Column('comment', db.Text)

    def __init__(self, job_id, comment):
        self.job_id = job_id
        self.comment = comment


class TimeStamp(db.Model):
    __tablename__ = "time_stamps"
    id = db.Column('id', db.Integer, primary_key=True)
    job_id = db.Column("job_id", db.Integer)
    description = db.Column('description', db.String)
    deadline = db.Column('deadline', db.Date)
    status = db.Column('status', db.Boolean)

    def __init__(self, job_id, description, deadline, status):
        self.job_id = job_id
        self.description = description
        self.deadline = deadline
        self.status = status