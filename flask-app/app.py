from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from report import User, getAllUsers, getWeb
import os
from dotenv import load_dotenv

load_dotenv()
GMAP_API_KEY = os.getenv("KEY")

app = Flask(__name__)
RASA_URI = "http://localhost:5005"


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def admin():
    return render_template("admin.html", name = 'admin')

@app.route('/home/<name>')
def userHome(name):
    return render_template("user.html", name = name, key = GMAP_API_KEY) 
    
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("pass")
    print(name)
    if(name == "admin" and password == "admin"):
        return redirect(url_for('admin'))
    else:
        return redirect(f'/home/{name}')

@app.route('/rasa', methods=['POST'])
def action():
    message = request.json
    print(f"User Message: {message}")
    res = requests.post(f"{RASA_URI}/webhooks/rest/webhook", json=message)
    # print(f"Bot Response : {res.json()}")
    return jsonify(res.json())

@app.route('/report', methods=['POST'])
def send():
    date = request.form.get("date")
    name = request.form.get("username")
    print(name, date)
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

@app.route('/website/<name>')
def getWebsite(name):
    url = getWeb(name)
    return {
        'url':url
    }


if __name__ == '__main__':
    app.run(debug=True)