from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'

class LandmarksForm(FlaskForm):
    Landmark_Name = StringField('Landmark Name:', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', display="", pageTitle='Landmarks')

@app.route('/add_Landmark', methods=['GET', 'POST'])
def add_Landmark():
    form = LandmarksForm()
    if form.validate_on_submit():
        return "<h2> The Landmark is {0}".format(form.Landmark_Name.data)

    return render_template('add_Landmark.html', form=form, pageTitle='Add new Landmark')

if __name__ == '__main__':
    app.run(debug=True)