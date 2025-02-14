from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class iperrilles_landmarksapp(db.Model):
    LandmarkID = db.Column(db.Integer, primary_key=True)
    LandmarkName = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Country = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Landmark Name: {1} | City: {2} | Country: {3}".format(self.LandmarkID, self.LandmarkName, self.City, self.Country)

class LandmarksForm(FlaskForm):
    LandmarkID = IntegerField('Landmark ID:')
    LandmarkName = StringField('Landmark Name:', validators=[DataRequired()])
    City = StringField('City:', validators=[DataRequired()])
    Country = StringField('Country:', validators=[DataRequired()])


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{}%".format(search_value)
        results = iperrilles_landmarksapp.query.filter(or_(iperrilles_landmarksapp.LandmarkName.like(search), iperrilles_landmarksapp.City.like(search), iperrilles_landmarksapp.Country.like(search))).all()
        return render_template('index.html', landmarks=results,pageTitle="Landmarks", legend="Search Results")
    else:
        return redirect('/')

@app.route('/')
def index():
    all_landmarks = iperrilles_landmarksapp.query.all()
    return render_template('index.html', landmarks = all_landmarks, pageTitle='Landmarks')

@app.route('/add_Landmark', methods=['GET', 'POST'])
def add_Landmark():
    form = LandmarksForm()
    if form.validate_on_submit():
        landmarks = iperrilles_landmarksapp(LandmarkName=form.LandmarkName.data,City=form.City.data,Country=form.Country.data)
        db.session.add(landmarks)
        db.session.commit()
        return redirect ('/')

    return render_template('add_Landmark.html', form=form, pageTitle='Add new Landmark')

@app.route('/delete_landmark/<int:LandmarkID>', methods=['GET','POST'])
def delete_landmark(LandmarkID):
    if request.method == 'POST': 
        LM_obj = iperrilles_landmarksapp.query.get_or_404(LandmarkID)
        db.session.delete(LM_obj)
        db.session.commit()
        flash('Landmark was successfully deleted!')
        return redirect("/")

    else: 
        return redirect("/")

@app.route('/landmark/<int:LandmarkID>', methods=['GET','POST'])
def get_landmark(LandmarkID):
    if request.method == 'POST': 
        LM_obj = iperrilles_landmarksapp.query.get_or_404(LandmarkID)
        return render_template('landmark.html', form=LM_obj, pageTitle='Landmark Details', legend="Landmark Details")
    else:
        LM_obj = iperrilles_landmarksapp.query.get_or_404(LandmarkID)
        return render_template('landmark.html', form=LM_obj, pageTitle='Landmark Details', legend="Landmark Details")

@app.route('/landmark/<int:LandmarkID>/update', methods=['GET','POST'])
def update_landmark(LandmarkID):
    LM_obj = iperrilles_landmarksapp.query.get_or_404(LandmarkID)
    form = LandmarksForm()

    if form.validate_on_submit():
        LM_obj.LandmarkID = form.LandmarkID.data
        LM_obj.LandmarkName = form.LandmarkName.data
        LM_obj.City = form.City.data
        LM_obj.Country = form.Country.data
        db.session.commit()
        flash('Landmark has been updated.')
        return redirect(url_for('get_landmark', LandmarkID=LM_obj.LandmarkID))
    else:
        form.LandmarkID.data = LM_obj.LandmarkID
        form.LandmarkName.data = LM_obj.LandmarkName
        form.City.data = LM_obj.City
        form.Country.data = LM_obj.Country
        return render_template('update_landmark.html', form=form, pageTitle='Update Landmark', legend="Update Landmark")


if __name__ == '__main__':
    app.run(debug=True)