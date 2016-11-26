"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os, sys
import bcrypt
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://patrycja:mypassword@localhost/todoapp'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)


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


###
# Routing for your application.
###
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/api/test')


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('/home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    print json_data
    user = User(
        email=json_data[u'email'],
        password=bcrypt.hashpw(json_data[u'password'].encode('utf-8'), bcrypt.gensalt())
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.checkpw(
            json_data['password'].encode('utf-8'), user.password.encode('utf-8')):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})


@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})


@app.route('/api/addjob', methods=['POST'])
def addjob():
    json_data = request.json
    job = Job(
        user_email=json_data['user_email'],
        company_name=json_data['company_name'],
        company_depart=json_data['company_depart'],
        position_title=json_data['position_title'],
        app_URL=json_data['app_URL']
    )
    try:
        db.session.add(job)
        db.session.commit()
        status = 'success'
    except:
        status = 'add job failed'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/deleteJob', methods=['POST'])
def deleteJob():
    json_data = request.json
    job_id = json_data['job_id']
    try:
        Job.query.filter_by(id=job_id).delete()
        db.session.commit()
        status = 'Delete job success. ID: %s .' % job_id
    except:
        status = 'Delete job failed. ID: %s .' % job_id
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/updateJob', methods=['POST'])
def updateJob():
    json_data = request.json
    job_id = json_data['job_id']
    updateItem = {}
    for key, value in json_data.items():
        if key != "job_id":
            updateItem[key] = value
    try:
        Job.query.filter_by(id=job_id).update(dict(updateItem))
        db.session.commit()
        status = 'update job success. ID: %s .' % job_id
    except:
        status = 'update job failed. ID: %s .' % job_id
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/addComment', methods=['POST'])
def addComment():
    json_data = request.json
    jobComment = Job_Comment(
        job_id=json_data['job_id'],
        comment=json_data['comment'],
    )
    try:
        db.session.add(jobComment)
        db.session.commit()
        status = 'success'
    except:
        status = 'add job failed'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/deleteComment', methods=['POST'])
def deleteComment():
    json_data = request.json
    comment_id = json_data['comment_id']
    try:
        Job_Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
        status = 'Delete comment success. ID: %s .' % comment_id
    except:
        status = 'Delete comment failed. ID: %s .' % comment_id
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/updateComment', methods=['POST'])
def updateComment():
    json_data = request.json
    comment_id = json_data['comment_id']
    updateItem = {'comment' : json_data['comment']}
    try:
        Job_Comment.query.filter_by(id=comment_id).update(dict(updateItem))
        db.session.commit()
        status = 'update comment success. ID: %s .' % comment_id
    except:
        status = 'update comment failed. ID: %s .' % comment_id
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/addTimeStamp', methods=['POST'])
def addTimeStamp():
    json_data = request.json
    timeStamp = TimeStamp(
        job_id=json_data['job_id'],
        description=json_data['description'],
        deadline=json_data['deadline'],
        status=json_data['status'],
    )

    try:
        db.session.add(timeStamp)
        db.session.commit()
        status = 'success'
    except:
        status = 'add event failed'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/deleteTimeStamp', methods=['POST'])
def deleteTimeStamp():
    json_data = request.json
    timestamp_id = json_data['event_id']
    try:
        TimeStamp.query.filter_by(id=timestamp_id).delete()
        db.session.commit()
        status = 'Delete timestamp success. ID: %s .' % timestamp_id
    except:
        status = 'Delete timestamp failed. ID: %s .' % timestamp_id
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/updateTimeStamp', methods=['POST'])
def updateTimeStamp():
    json_data = request.json
    timestamp_id = json_data['event_id']
    updateItem = {}
    for key, value in json_data.items():
        if key != 'event_id':
            updateItem[key] = value
    try:
        TimeStamp.query.filter_by(id=timestamp_id).update(dict(updateItem))
        db.session.commit()
        status = 'update TimeStamp success. ID: %s .' % timestamp_id
    except:
        status = 'update TimeStamp failed. ID: %s .' % timestamp_id
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/getAllJobs', methods=['GET'])
def getAllJobs():
    user_email = request.args.get('user_email').encode('utf-8')
    res = {"user_email": user_email,
           "jobs": []}
    try:
        for job in Job.query.filter_by(user_email=user_email).all():
            job_entry = {
                "company_name": job.company_name,
                "company_depart": job.company_depart,
                "position_title": job.position_title,
                "app_URL": job.app_URL,
                "time_stamps": [],
                "comments": []
            }
            for timestamp in TimeStamp.query.filter_by(job_id=job.id).all():
                timestamp_entry = {
                    "id": timestamp.id,
                    "job_id": timestamp.job_id,
                    "description": timestamp.description,
                    "deadline": timestamp.deadline,
                    "status": timestamp.status
                }
                job_entry["time_stamps"].append(timestamp_entry)
            for comment in Job_Comment.query.filter_by(job_id=job.id).all():
                comment_entry = {
                    "id": comment.id,
                    "job_id": comment.job_id,
                    "comment": comment.comment
                }
                job_entry["comments"].append(comment_entry)
            res["jobs"].append(job_entry)
        status = 'success'
    except:
        status = 'query job failed'
    db.session.close()
    return jsonify({
        "status": status,
        "user_info": res
    })

@app.route('/api/getJobList', methods=['GET'])
def getJobList():
    user_email = request.args.get('user_email').encode('utf-8')
    res = {"user_email": user_email,
           "job_list": []}
    try:
        for job in Job.query.filter_by(user_email=user_email).all():
            job_entry = {
                "job_id" : job.id,
                "company_name": job.company_name,
                "company_depart": job.company_depart,
                "position_title": job.position_title,
                "app_URL": job.app_URL,
            }
            res["job_list"].append(job_entry)
        status = 'success'
    except:
        status = 'query job failed'
    db.session.close()
    return jsonify({
        "status": status,
        "jobs": res
    })


@app.route('/api/getTimeStamps', methods=['GET'])
def getTimeStamps():
    job_id = request.args.get('job_id').encode('utf-8')
    res = {"job_id": job_id,
           "timeStamp_list": []}
    try:
        for timestamp in TimeStamp.query.filter_by(job_id=job_id).all():
            timestamp_entry = {
                "id": timestamp.id,
                "job_id": timestamp.job_id,
                "description": timestamp.description,
                "deadline": timestamp.deadline,
                "status": timestamp.status
            }
            res["timeStamp_list"].append(timestamp_entry)
        status = 'success'
    except:
        status = 'query job failed'
    db.session.close()
    return jsonify({
        "status": status,
        "timeStamps": res
    })

@app.route('/api/getTimeStamp', methods=['GET'])
def getTimeStamp():
    event_id = request.args.get('event_id').encode('utf-8')
    res = {"event_id": event_id,
           "info": {}}
    try:
        for timestamp in TimeStamp.query.filter_by(id=event_id).all():
            timestamp_entry = {
                "id": timestamp.id,
                "job_id": timestamp.job_id,
                "description": timestamp.description,
                "deadline": timestamp.deadline,
                "status": timestamp.status
            }
            res["info"] = timestamp_entry
        status = 'success'
    except:
        status = 'query job failed'
    db.session.close()
    return jsonify({
        "status": status,
        "timeStamps": res
    })

@app.route('/api/getUndoTimeStamp', methods=['GET'])
def getUndoTimeStamp():
    user_email = request.args.get('user_email').encode('utf-8')
    res = {"user_email": user_email,
           "timeStamp_list": []}
    try:
        jobIDs = []
        for job in Job.query.filter_by(user_email=user_email).all():
            jobIDs.append(job.id)
        for job_id in jobIDs:
            for timestamp in TimeStamp.query.filter_by(job_id=job_id).all():
                if timestamp.status:
                    continue
                timestamp_entry = {
                    "id": timestamp.id,
                    "job_id": timestamp.job_id,
                    "description": timestamp.description,
                    "deadline": timestamp.deadline,
                    "status": timestamp.status
                }
                res["timeStamp_list"].append(timestamp_entry)
        status = 'success'
    except:
        status = 'query event failed'
    db.session.close()
    return jsonify({
        "status": status,
        "res": res
    })

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
