#!/usr/bin/python
from flask import Blueprint, render_template

app = Blueprint('landing', __name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

