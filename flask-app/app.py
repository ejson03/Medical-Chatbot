from flask import Flask, render_template, request, jsonify, redirect, url_for, abort, session, make_response, flash
import requests
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_mongo_sessions import MongoDBSessionInterface
from modules import *
from time import sleep
import os
from io import BytesIO
from os import system, environ
import jwt, json, asyncio
import bcrypt
from functools import partial


MONGO_URL = environ.get("MONGODB_STRING")  
GMAP_API_KEY = environ.get("KEY")
SECRET_KEY = environ.get("SECRET_KEY")
RASA_URI = "http://localhost:5005"

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_DBNAME'] = 'authenticate'
app.config['MONGO_URI'] = f"{MONGO_URL}/authenticate"
cors = CORS(app)
mongo = PyMongo(app)

with app.app_context():
    app.session_interface = MongoDBSessionInterface(app, mongo.db, 'sessions')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

async def jwt_sess_auth(message):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, partial(requests.post,f"{RASA_URI}/webhooks/token/webhook",json=message))
    res = await future
    res = json.loads(res.text)
    session['token']=  res['bot_token']

async def trigger_action(action, name):
    data = {
        "user": name,
        "name": action,
        "policy": "MappingPolicy", 
        "confidence": "0.98"
    }
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, partial(requests.post, f"{RASA_URI}/conversations/{name}/execute", json=data))
    res = await future
    print("Response from action is", res)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/home')
def user():
    if 'username' in session:    
        return render_template("index.html", key = GMAP_API_KEY)
    else:
        flash("Your session has expired")
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("pass")
    if(name == "admin" and password == "admin"):
        message = {'sender' : name, 'role': 'admin'}
        session['username'] = name
        return redirect(url_for('admin'))
    else:
        users = mongo.db.users
        login_user = users.find_one({'name' : name})
        if login_user:
            if bcrypt.hashpw(password.encode('utf-8'), login_user['password'].decode().encode('utf-8')) == login_user['password'].decode().encode('utf-8'):
                session['username'] = name
                message = {'sender' : name, 'role': 'user'}
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(jwt_sess_auth(message))
                loop.run_until_complete(trigger_action('action_get_credentials', name))
                return redirect(url_for('user'))
            else:
                flash("Wrong Password !")
                return redirect(url_for('index'))
        else:
            flash("User does not exists..Please Sign Up !")
            return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        password = request.form.get("pass")

        if(name == "admin" and password == "admin"):
            message = {'sender' : name, 'role': 'admin'}
            session['username'] = name
            return redirect(url_for('admin'))
        else:
            users = mongo.db.users
            existing_user = users.find_one({'name' : name})
            if existing_user is None:
                hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                users.insert_one({'name' : name, 'password' : hashpass})
                session['username'] = name
                message = {'sender' : name, 'role': 'user'}
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(jwt_sess_auth(message))
                loop.run_until_complete(trigger_action('action_get_credentials', name))
                return redirect(url_for('user'))
            else:
                flash("User already exists... !")
                return redirect(url_for('signup'))

    
@cross_origin() 
@app.route('/rasa', methods=['POST'])
def action():
    if 'token' in session:
        try:
            files = request.files['file']
            print(files.mimetype)
            files = {"file": (files.filename, files.stream, files.mimetype)}
            res = requests.post(f"{RASA_URI}/webhooks/rest/webhook", files=files, headers={'Authorization': session['token']})
            print(res.json())
        except:
            message = request.json
            res = requests.post(f"{RASA_URI}/webhooks/rest/webhook", json=message, headers={'Authorization': session['token']})
        return jsonify(res.json())
    else:
        flash("The token is wrong")

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
    if 'username' in session:
        session.clear()
        return render_template('login.html')
    else:
        flash("You have already sign out")
        return redirect(url_for('index'))
    


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

if __name__ == '__main__':
    # context = ('server.crt', 'server.key')
    # app.run(host='0.0.0.0', debug=True, ssl_context=context)
    app.secret_key = 'mysecret'
    app.run(debug=True, threaded=True)
