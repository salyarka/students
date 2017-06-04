from flask import render_template, redirect, url_for
from .forms import StudentForm, DisciplineForm
from app import app, db


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/discipline', methods=['GET', 'POST'])
def discipline():
    discipline = db.get_model('Discipline')
    disciplines = discipline.get()
    form = DisciplineForm()
    if form.validate_on_submit():
        return redirect(url_for('discipline'))
    return render_template(
        'discipline.html', disciplines=disciplines, form=form
    )


@app.route('/discipline/<int:identificator>', methods=['DELETE'])
def del_discipline(identificator):
    discipline = db.get_model('Discipline')
    discipline.remove(identificator)
    db.commit()
    return redirect(url_for('discipline'))


@app.route('/student', methods=['GET', 'POST'])
def student():
    student = db.get_model('Student')
    students = student.get()
    form = StudentForm()
    if form.validate_on_submit():
        return redirect(url_for('student'))
    return render_template('student.html', students=students, form=form)


@app.route('/student/<int:identificator>', methods=['DELETE'])
def del_student(identificator):
    student = db.get_model('Student')
    student.remove(identificator)
    db.commit()
    return redirect(url_for('student'))
