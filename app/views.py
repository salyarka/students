from flask import render_template, redirect, url_for
from .forms import StudentForm, DisciplineForm
from app import app, db


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/discipline', methods=['GET', 'POST'])
def discipline():
    disciplines = [1,2,3]
    form = DisciplineForm()
    if form.validate_on_submit():
        return redirect(url_for('discipline'))
    return render_template(
        'discipline.html', disciplines=disciplines, form=form
    )


@app.route('/student', methods=['GET', 'POST'])
def student():
    students = ['jaba', 'baba']
    form = StudentForm()
    if form.validate_on_submit():
        return redirect(url_for('student'))
    return render_template('student.html', students=students, form=form)
