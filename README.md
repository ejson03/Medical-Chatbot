# Medical Analytica
A therapy based chatbot for emotion analysis and visualization

# Table of Contents

* [Description](https://github.com/ejson03/Medical-Analytica#description)
* [Dependencies](https://github.com/ejson03/Medical-Analytica#dependencies)
* [Installation](https://github.com/ejson03/Medical-Analytica#installation)
  * [Prerequisites](https://github.com/ejson03/Medical-Analytica#prerequisites)
  * [Instructions](https://github.com/ejson03/Medical-Analytica#instructions)
* [Usage](https://github.com/ejson03/Medical-Analytica#usage)
* [Contributors](https://github.com/ejson03/Medical-Analytica#contributors)
* [License](https://github.com/ejson03/Medical-Analytica#license)

# Description

There is a wave of emotional unstabiltiy among people who are on a downward spiral in life or are going through hard times. We have developed a chat companion to make the user feel better and to track analysis of users behaviour.


### Chatbot replying with a joke & quote
![Joke](images/joke.png)

### Chatbot playing a youtube music video based on user emotion
![Video](images/video.png)

### Chatbot displaying neaby hospitals with information
![Map](images/map.png)

### Organization can keep record of patients weekly analysis
![chart](images/chart.png)

Additional features include weather reporting, self genearted inspirational quotes, yet to implement symptom checker and analysis

# Dependencies

* [Rasa](https://rasa.com/)
* [MongoDB](https://www.mongodb.com/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Python](https://www.python.org/)


# Installation

### Prerequisites
Install Python and MongoDB from the above links

### Instructions

Clone the repository
```
git clone https://github.com/ejson03/Medical-Analytica.git
```

Setup Python environment
```
python -m venv venv

[Windows users]
.\venv\Scripts\activate

[Ubuntu]
source venv/bin/activate

pip install -r requirements.txt
```

For training and testing
```
cd chatbot
rasa train
rasa test
```

Running in one command
```
python setup.py
```

# Usage

Open a browser and go to 
```
http://localhost:5000
```
# Contributors

* Elvis Dsouza [@ejson03](https://github.com/ejson03)
* Vedant Sahai [@Vedantsahai18](https://github.com/Vedantsahai18)

# License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[MIT License Link](https://github.com/ejson03/Medical-Analytica/blob/master/LICENSE)





