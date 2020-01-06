
from flask import Flask, flash, render_template, request, jsonify, redirect
import logging
from logging import Formatter, FileHandler
from forms import *
import os, requests, json
import random 
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
        patient_data = {
                         'id': random.randint(0, 100000),
                         'email': form.email.data, 
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
    diab_url = 'https://flask-db-api.herokuapp.com/diabetes/diabetes_history'
    can_url = 'https://flask-db-api.herokuapp.com/cancer'
    heart_url = 'https://flask-db-api.herokuapp.com/heart'

    diab_request = requests.get(url=diab_url)
    diab_records = diab_request.json()

    can_request = requests.get(url=can_url)
    can_records = can_request.json()
    print(can_records)
    
    heart_request = requests.get(url=heart_url)
    heart_records = heart_request.json()

    dpos = 0
    dneg = 0

    cpos = 0
    cneg = 0

    hpos = 0
    hneg = 0

    diab_ages = []
    can_ages = []
    heart_ages = []

    diab_bmis = []
    can_bmis = []

    heart_chols = []

    for record in diab_records: 
        if record['prediction'] == 1:
            dpos += 1
            diag_ages.append(record['age'])
            diab_bmis.append(record['bmi'])
        elif record['prediction'] == 0:
            dneg += 1 
    
    for record in can_records['data']: 
        if record['prediction'] == 1:
            cpos += 1
            can_ages.append(record['age'])
            can_bmis.append(record['bmi'])
        elif record['prediction'] == 0:
            cneg += 1 

    for record in heart_records['data']: 
        if record['prediction'] == 1:
            hpos += 1
            heart_ages.append(record['age'])
            heart_chols.append(record['cholesterol'])
        elif record['prediction'] == 0:
            hneg += 1 

    diab_age_mean, can_age_mean, heart_age_mean = 0,0,0
    diab_bmi_mean, can_bmi_mean = 0,0
    dpercent, cpercent, hpercent = 0,0,0

    if len(diab_ages)!=0: diab_age_mean = sum(diab_ages) / len(diab_ages)
    if len(can_ages)!=0: can_age_mean = sum(can_ages) / len(can_ages)
    if len(heart_ages)!=0: heart_age_mean = sum(heart_ages) / len(heart_ages)

    if len(diab_bmis)!=0: diab_bmi_mean = sum(diab_bmis) / len(diab_bmis)
    if len(can_bmis)!=0: can_bmi_mean = sum(can_bmis) / len(can_bmis)

    if len(heart_chols)!=0: heart_chol_mean = sum(heart_chols) / len(heart_chols)

    if dpos!=0: dpercent = int(dpos / (dpos + dneg) * 100)
    if cpos!=0: cpercent = int(cpos / (cpos + cneg) * 100)
    if hpos!=0: hpercent = int(hpos / (hpos + hneg) * 100)

    stats = {
        'diab_age_mean': diab_age_mean,
        'can_age_mean': can_age_mean,
        'heart_age_mean': heart_age_mean,
        'diab_bmi_mean': diab_bmi_mean,
        'can_bmi_mean': can_bmi_mean,
        'dpercent': dpercent,
        'cpercent': cpercent,
        'hpercent': hpercent,
        'heart_chol_mean': heart_chol_mean
    }

    return render_template('pages/UserProfiling.html',dpos=dpos, dneg=dneg, cpos=cpos, cneg=cneg, hpos=hpos, hneg=hneg, stats=stats)

@app.route('/medi_Ai_Interface', methods=['POST', 'GET'])
def medi_ai_interface():
    form = SearchRecordsForm()
    records = {}
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        api_url = 'https://flask-db-api.herokuapp.com/diabetes/patient_history/' + first_name + "/" + last_name
        result = requests.get(url=api_url)
        records = result.json()
        print(result)
        if result.ok:
            print(result.text)
            flash("Got the data!")
        else:
            flash('Error')
    else:
        flash('Account couldn\'t be created')
        print('"ERROR"')
    return render_template('pages/Medi_AI_Interface.html', records=records, form=form)

@app.route('/HeartDiseases')
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
