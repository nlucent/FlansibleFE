# __init__.py
# Kicks off flask server
# Nick Lucent

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views

