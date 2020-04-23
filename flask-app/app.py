from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import re
import requests
from report import User

app = Flask(__name__)
RASA_URI = "http://localhost:5005"


def get_url(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("https://www.youtube.com/embed/" + search_results[0])
    url = "https://www.youtube.com/embed/" + search_results[0]
    return url

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get("name")
    password = request.form.get("pass")
    print(name, password)
    if(name == "admin" and password == "admin"):
        return render_template("admin.html")
    else:
        return render_template("user.html")

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
    name = request.form.get("name")
    user - User(name)
    data = user.weeklyReport(date)
    return {name: data.tolist()}



if __name__ == '__main__':
    app.run(debug=True)