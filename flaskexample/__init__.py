from flask import Flask
app = Flask(__name__)
from flaskexample import views

app.config.from_pyfile('default.cfg')
