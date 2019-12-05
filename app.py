
from flask import Flask, flash, render_template, request, jsonify, redirect
import logging
from logging import Formatter, FileHandler
from forms import *
import os, requests, json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object('config')


@app.route('/index')
def index():
    return render_template('pages/placeholder.home.html')

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    api_url = 'https://flask-db-api.herokuapp.com/patient/'
    # api_url = 'http://127.0.0.1:5010/patient/'

    if form.validate_on_submit():
        hashed_pass = generate_password_hash(form.password.data)
        patient_data = { 
                         'username': form.username.data, 
                         'password': form.password.data, 
                        }
        result = requests.get(url=api_url, json=patient_data)
        print(result)
        if result.ok:
            print(result.text)
            flash("Logged in!")
            return redirect('index')
        else:
            flash('')
    else:
        flash('There are errors in your form.')
        print('"ERROR"')

    # return render_template('pages/placeholder.home.html', form=form)
    # else:
    # print("Something went wrong")
    return render_template('forms/login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    api_url = 'https://flask-db-api.herokuapp.com/patient/'
    # api_url = 'http://127.0.0.1:5010/patient/'

    if form.validate_on_submit():
        patient_data = { 'email': form.email.data, 
                         'username': form.username.data, 
                         'first_name': form.first_name.data, 
                         'last_name': form.last_name.data, 
                         'password': form.password.data,
                         'profession': form.profession.data 
                         }
        result = requests.post(url=api_url, json=patient_data)
        print(result)
        if result.ok:
            print(result.text)
            flash("Account created!")
            return redirect('index')
        else:
            flash('')
    else:
        flash('Account couldn\'t be created')
        print('"ERROR"')
    return render_template('forms/register.html', form=form)


@app.route('/accessRestrictions')
def accessRestrictions():
    return render_template('pages/accessRestrictions.html')



@app.route('/cancer')
def cancer():
    return render_template('pages/cancer.html')

@app.route('/diabetes')
def diabetes():
    return render_template('pages/diabetes.html')

@app.route('/user_profiling')
def user_profiling():
    records = {"times_pregnant": "2", "glucose": "16.5", "blood_pressure": "110", "skin_fold": "1.25", "bmi": "30.2", "ped_function": "4", "age": "25"}, {"times_pregnant": "4", "glucose": "45", "blood_pressure": "120", "skin_fold": "2.2", "bmi": "25.2", "ped_function": "2", "age": "55"}

    return render_template('pages/UserProfiling.html', records=records)

@app.route('/medi_Ai_Interface')
def medi_ai_interface():
    return render_template('pages/Medi_AI_Interface.html')

@app.route('/aggregationOfNewPatientData.html')
def aggregationOfNewPatientData():
    return render_template('pages/aggregationOfNewPatientData.html')

@app.route('/heartDiseases')
def heartDiseases():
    return render_template('pages/heartDiseases.html')
    
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# @app.route('/handle_data', methods=['POST'])
# def handle_data():
#     if request.method == 'POST':
#         # projectpath = request.form['projectFilepath']
#         # print(projectpath)
#         mail = form.projectFilepath.username
#         print(mail)
#         # requests.post('https://flask-db-api.herokuapp.com/patinet').content
#         return render_template("pages/placeholder.home.html"), 200
#     else:
#         return render_template("pages/placeholder.home.html"), 200

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run(debug=True)
