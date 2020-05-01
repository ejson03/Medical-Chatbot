from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from flask_cors import CORS, cross_origin
from report import User, getAllUsers, getWeb
import os
from dotenv import load_dotenv

load_dotenv()
GMAP_API_KEY = os.getenv("KEY")

app = Flask(__name__)
RASA_URI = "http://localhost:5005"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template("admin.html", name = 'admin')

@app.route('/home/<name>')
def user(name):
    return render_template("user.html", name = name, key = GMAP_API_KEY) 
    
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("pass")
    if(name == "admin" and password == "admin"):
        return redirect(url_for('admin'))
    else:
        return redirect(f'/home/{name}')

@cross_origin()
@app.route('/rasa', methods=['POST'])
def action():
    message = request.json
    print(message)
    res = requests.post(f"{RASA_URI}/webhooks/rest/webhook", json=message)
    print(res)
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

@app.route('/showmap/<name>')
def showmap(name):
    return render_template('map.html', name = name, key = GMAP_API_KEY)


if __name__ == '__main__':
    app.run(debug=True)