from flask import render_template
from app import app


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/discipline')
def discipline():
    return render_template('discipline.html')


@app.route('/student')
def student():
    return render_template('student.html')
