from flask import Flask, render_template, session, redirect, url_for, request, send_file, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired

from calculate import Calculate

from handle_csv import Datasheet


app = Flask(__name__)

app.config['SECRET_KEY'] = 'key'

class InfoForm(FlaskForm):
    file = FileField('file')
    age = StringField('What is your age ? ')
    sex = SelectField('Gender: ', choices = [('1','Male'), ('0', 'Female')] )
    bmi = StringField('What is your BMI ? ')
    smoker = SelectField('Are you a smoker ? ', choices = [('1','Yes'), ('0', 'No')] )
    children = StringField('How many children do you have ? ')
    region = SelectField('Which region are you from ? ', 
                            choices = [('0','NorthEast'), ('1', 'NorthWest'), ('2', 'SouthEast'), ('3', 'SouthWest')] )
    sub = SubmitField('Submit')



@app.route('/',methods = ['GET', 'POST'])
def index():
    form = InfoForm()
    print(form.errors)
    
    if form.validate_on_submit():
        print("submit")
        if form.file.data:
            print("if")
            Datasheet(form.file.data).compute()
            return redirect(url_for('download'))
        else:
            print("else")
            session['age'] = form.age.data
            session['sex'] = form.sex.data
            session['bmi'] = form.bmi.data
            session['smoker'] = form.smoker.data
            session['children'] = form.children.data
            session['region'] = form.region.data
            return redirect(url_for('expenses'))
        
    return render_template('index.html', form = form)


@app.route('/expenses')
def expenses():
    age = float(session['age'])
    sex = int(session['sex'])
    bmi = float(session['bmi'])
    smoker = int(session['smoker'])
    children = int(session['children'])
    region = int(session['region'])
    
    total = Calculate(age, sex, bmi, smoker, children, region).calculate()
    return render_template('expenses.html',total = total)


@app.route('/return-file/')
def return_file():
    return send_from_directory('\\Users\\Kartheek\\Desktop\\env\\insurance_final\\static\\','expenses.csv', as_attachment=True)

@app.route('/download/', methods = ['GET', 'POST'])
def download():
    return render_template('download.html')

if __name__ == '__main__':
    app.run(debug=True)