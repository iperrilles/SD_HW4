from flask import Flask
from flask import render_template, redirect,request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

#dbuser = os.environ.get('DBUSER')
#dbpass = os.environ.get('DBPASS')
#dbhost = os.environ.get('DBHOST')
#dbname = os.environ.get('DBNAME')

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class iperrilles_landmarksapp(db.Model):
    LandmarkID = db.Column(db.Integer, primary_key=True)
    LandmarkName = db.Column(db.String(255))
    City = db.Column(db.String(255))
    Country = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Landmark Name: {1} | City: {2} | Country: {3}".format(self.LandmarkID, self.LandmarkName, self.City, self.Country)

class LandmarksForm(FlaskForm):
    Landmark_Name = StringField('Landmark Name:', validators=[DataRequired()])
    City = StringField('City:', validators=[DataRequired()])
    Country = StringField('Country:', validators=[DataRequired()])


@app.route('/')
def index():
    all_landmarks = iperrilles_landmarksapp.query.all()
    return render_template('index.html', landmarks = all_landmarks, pageTitle='Landmarks')

@app.route('/add_Landmark', methods=['GET', 'POST'])
def add_Landmark():
    form = LandmarksForm()
    if form.validate_on_submit():
        landmarks = iperrilles_landmarksapp(LandmarkName=form.Landmark_Name.data,City=form.City.data,Country=form.Country.data)
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
        return render_template('landmark.html', form=landmark, pageTitle='Landmark Details')


if __name__ == '__main__':
    app.run(debug=True)