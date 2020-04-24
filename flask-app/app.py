from flask import Flask, render_template, request, jsonify
import requests
from report import User, getAllUsers

app = Flask(__name__)
RASA_URI = "http://localhost:5005"


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def admin():
    return render_template("admin.html", name = 'admin')
    
@app.route('/login', methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("pass")
    print(name)
    if(name == "admin" and password == "admin"):
        return render_template("admin.html", name = 'admin')
    else:
        return render_template("user.html", name = name)

@app.route('/rasa', methods=['POST'])
def action():
    message = request.json
    print(f"User Message: {message}")
    res = requests.post(f"{RASA_URI}/webhooks/rest/webhook", json=message)
    print(f"Bot Response : {res.json()}")
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


if __name__ == '__main__':
    app.run(debug=True)