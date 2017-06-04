from flask import render_template, redirect, url_for, request, flash
from .forms import StudentForm, DisciplineForm
from app import app, db


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/discipline', methods=['GET', 'POST'])
def discipline():
    discipline = db.get_table('discipline')
    disciplines = discipline.get()
    form = DisciplineForm()
    if form.validate_on_submit():
        discipline.add(form.title.data)
        db.commit()
        return redirect(url_for('discipline'))
    return render_template(
        'discipline.html', disciplines=disciplines, form=form
    )


@app.route('/discipline/<int:identificator>', methods=['DELETE'])
def del_discipline(identificator):
    discipline = db.get_table('discipline')
    discipline.remove(identificator)
    db.commit()
    return redirect(url_for('discipline'))


@app.route('/discipline/<int:identificator>', methods=['PUT'])
def update_discipline(identificator):
    new_title = request.args.get('title')
    if new_title:
        discipline = db.get_table('discipline')
        discipline.update(identificator, new_title)
        db.commit()
    return redirect(url_for('discipline'))


@app.route('/student', methods=['GET', 'POST'])
def students():
    student = db.get_table('student')
    students = student.get()
    form = StudentForm()
    if form.validate_on_submit():
        student.add(form.name.data, form.surname.data)
        db.commit()
        return redirect(url_for('students'))
    return render_template('students.html', students=students, form=form)


@app.route('/student/<int:identificator>', methods=['GET', 'POST'])
def student(identificator):
    student_model = db.get_table('student')
    discipline = db.get_table('discipline')
    student = student_model.get(identificator)
    disciplines = discipline.get()
    scores = student_model.get_scores(identificator)
    for each in disciplines:
        if each['id'] not in scores:
            scores[each['id']] = {'score': '', 'id': 0}
    form = StudentForm()
    if form.validate_on_submit():
        student.update(identificator, new_name, new_surname)
        db.commit()
        return redirect(url_for('student'))
    return render_template(
        'student.html', student=student,
        form=form, disciplines=disciplines,
        scores=scores
    )


@app.route('/student/<int:identificator>', methods=['DELETE'])
def del_student(identificator):
    student = db.get_table('student')
    student.remove(identificator)
    db.commit()
    return redirect(url_for('students'))


@app.route('/student/<int:identificator>', methods=['PUT'])
def update_student(identificator):
    new_name = request.args.get('name')
    new_surname = request.args.get('surname')
    if new_name and new_surname:
        student = db.get_table('student')
        student.update(identificator, new_name, new_surname)
        db.commit()
    return redirect(url_for('student', identificator=identificator))


@app.route(
    '/student/<int:identificator>/<int:discipline>/<int:score_id>',
    methods=['PUT']
)
def set_score(identificator, discipline, score_id):
    new_score = request.args.get('update_score')
    if new_score:
        try:
            if int(new_score) in range(1, 6):
                student = db.get_table('student')
                student.set_score(
                    new_score, discipline, identificator, int(score_id)
                )
                db.commit()
        except ValueError:
            pass
    return redirect(url_for('student', identificator=identificator))


@app.route('/student/<int:identificator>/<int:score_id>/', methods=['PATCH'])
def unset_score(identificator, score_id):
    student = db.get_table('student')
    student.unset_score(score_id)
    db.commit()
    return redirect(url_for('student', identificator=identificator))
