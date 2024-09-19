from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import uuid
from datetime import datetime, timedelta
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)

UPLOAD_FOLDER = './static/images'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

leader_club = db.Table('leader_club',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

user_club = db.Table('user_club',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

club_tag = db.Table('club_tag',
    db.Column('club_id', db.Integer, db.ForeignKey('club.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False)
    myClubs = db.relationship('Club', secondary=leader_club, backref='admins', lazy="dynamic")
    clubs = db.relationship('Club', secondary=user_club, backref='members', lazy="dynamic")
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    clubname = db.Column(db.Text, nullable=False)
    mission = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    imgName = db.Column(db.Text, unique=True, nullable=False)
    events = db.relationship('Event', backref='club')
    tags = db.relationship('Tag', secondary=club_tag, backref='club', lazy="dynamic")

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.Text, nullable=False)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user, request.form['remember'])
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = '/'
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash('Email already registered')
            return render_template('register.html')
        if request.form['password']==request.form['password2']:
            user = User(email=request.form['email'],
                        password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('You can now login.')
            return redirect('/login')
        else:
            flash('passwords must match')
    return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    clubs = current_user.clubs.all()
    eventDict = {}
    today=datetime.now()
    events = Event.query.join(Club).filter(Club.id.in_([c.id for c in clubs])).order_by(Event.datetime)
    for i in range(-31,32):
        day=today+timedelta(i)
        datestring=day.strftime("%A, %B %d")
        dayEvents = []
        #events=Event.query.filter(func.date(Event.datetime)==func.date(day)).order_by(Event.datetime)
        for event in events:
            if event.datetime.date()==day.date():
                dayEvents.append(event)
        eventDict[i]=dict(datestring=datestring, events=dayEvents)

    eDictjs = {}
    for event in events:
        eDictjs[str(event.id)]=dict(eventSubject=event.subject, eventDescription=event.description, eventLocation=event.location, clubName=event.club.clubname)

    return(render_template("index.html", eventDict=eventDict, eDictjs=json.dumps(eDictjs)))

@app.route('/search', methods=['POST', 'GET'])
@login_required
def clubSearch():
    if request.method=='POST':
        myClub = Club.query.get(request.form['clubID'])
        myUser = current_user
        if request.form['isFollow']=='true':
            myUser.clubs.remove(myClub)
        else:
            myUser.clubs.append(myClub)
        try:
            db.session.add(myUser)
            db.session.commit()
            return redirect('/search')
        except:
            return 'There was an issue adding your entry'
        
    myUser = current_user
    clubs = Club.query.all()
    clubDict = {}
    for club in clubs:
        isFollowed="false"
        if myUser.clubs.filter(user_club.c.club_id == club.id).count()>0:
            isFollowed="true"
        clubDict[str(club.id)]=dict(clubname=club.clubname, mission=club.mission, description=club.description, imgName=club.imgName, isFollowed=isFollowed)

    return(render_template("clubSearch.html", clubs=clubs, clubDict=json.dumps(clubDict), currentUser=current_user))

@app.route('/leader', methods=['POST', 'GET'])
@login_required
def leaderMenu():
    if request.method== 'POST':
        if request.form['formType']=='editor':
            myClub = Club.query.get(request.form['clubID'])
            myClub.clubname=request.form['club-name']
            myClub.description=request.form['club-description']
            myClub.mission=request.form['club-mission']
            clubPic=request.files['upload']
            if clubPic:
                filename = uuid.uuid4().hex
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], myClub.imgName))
                clubPic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                myClub.imgName=filename
            db.session.add(myClub)
            db.session.commit()
            return redirect('/leader')
           
        elif request.form['formType']=='scheduler':
            myClub = Club.query.get(request.form['clubID'])
            eventDate=request.form['date']
            eventTime=request.form['time']
            eventDateTime=datetime.strptime(eventDate+" "+eventTime,'%Y-%m-%d %H:%M')
            newEvent=Event(datetime=eventDateTime, subject=request.form['meeting-subject'], description=request.form['meeting-description'], location=request.form['meeting-location'], club=myClub)
            try:
                db.session.add(newEvent)
                db.session.commit()
                return redirect('/leader')
            except:
                return 'There was an issue adding your entry'
        elif request.form['formType']=='creater':
            clubname=request.form['club-name']
            clubDescription=request.form['club-description']
            clubMission=request.form['club-mission']
            clubPic=request.files['upload']
            if clubPic.filename == '':
                filename='images-empty.png'
            if clubPic:
                filename = uuid.uuid4().hex
                clubPic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newClub = Club(clubname=clubname, mission=clubMission, description=clubDescription, imgName=filename)
            try:
                db.session.add(newClub)
                myUser = current_user
                myUser.myClubs.append(newClub)
                myUser.clubs.append(newClub)
                db.session.add(myUser)
                db.session.commit()
                return redirect('/leader')
            except:
                return 'There was an issue adding your entry'
    clubs = current_user.myClubs.all()
    clubDict = {}
    for club in clubs:
        clubDict[str(club.id)]=dict(clubname=club.clubname, mission=club.mission, description=club.description, imgName=club.imgName)
    return(render_template("leaderMenu.html", clubs=clubs, clubDict=json.dumps(clubDict)))

if __name__ == "__main__":
    app.run(debug=True)