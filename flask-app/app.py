from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from flask_cors import CORS, cross_origin
from modules.report import User, getAllUsers, getWeb
from modules.session import Session
import os
from os import system, environ
import jwt, json

GMAP_API_KEY = environ.get("KEY")
SECRET_KEY = environ.get("SECRET_KEY")
RASA_URI = "http://localhost:5005"

app = Flask(__name__)
session = Session()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def jwt_sess_auth(message):
    res = requests.post(f"{RASA_URI}/webhooks/token/webhook", json=message)
    res = res.json()
    session.set(res['bot_token'])

def jwt_decode(token):
    query = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return query

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template("admin.html", name = 'admin')

@app.route('/home')
def user():
    return render_template("user.html", key = GMAP_API_KEY) 
  
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("pass")

    if(name == "admin" and password == "admin"):
        message = {'sender' : name, 'role': 'admin'}
        jwt_sess_auth(message)
        return redirect(url_for('admin'))
    else:
        message = {'sender' : name, 'role': 'user'}
        jwt_sess_auth(message)
        return redirect(url_for('user'))

@cross_origin() 
@app.route('/rasa', methods=['POST'])
def action():
    message = request.json
    message['sender'] = jwt_decode(session.get())['user_id']
    res = requests.post(f"{RASA_URI}/webhooks/rest/webhook", json=message, headers={'Authorization': session.get()})
    return jsonify(res.json())

@app.route('/report', methods=['POST'])
def send():
    date = request.form.get("date")
    name = request.form.get("username")
    user = User(name)
    data = user.weeklyReport(date)
    return {
        'name': data
    }

@app.route('/users', methods=['GET'])
def getUsers():
    users = getAllUsers()
    print(users)
    return {
        'users': users
    }

@app.route('/users/<user>', methods=['GET'])
def page(user):
    return render_template('admin.html', name = user)

@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/retrain/<name>')
def retrain(name):
    user = User(name)
    user.generateStory()

@app.route('/website/<query>')
def getWebsite(query):
    url = getWeb(query)
    return {
        'url':url
    }

@app.route('/showmap')
def showmap():
    return render_template('map.html', key = GMAP_API_KEY)

@app.route('/uploads', methods=['POST'])
def upload():
    if request.method == 'POST':
        data = request.files['file']
        name = jwt_decode(session.get())['user_id']
        if not os.path.exists(f'uploads/{name}'):
            os.makedirs(f'uploads/{name}')
        data.save(f'uploads/{name}/{data.filename}')
        return jsonify({'response': 'File uploaded success!'})
    else:
        abort(404)


if __name__ == '__main__':
    _ = system('cls') 
    app.run(debug=True)
    
    # for docker
    #context = ('server.crt', 'server.key')
    #app.run(host='0.0.0.0', debug=True, ssl_context=context)