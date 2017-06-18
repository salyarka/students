from flask import render_template, redirect, url_for, request, abort
from .forms import StudentForm, DisciplineForm, SearchForm
from .paginator import Paginator
from app import app, db


PER_PAGE = 15 # Number of students in pages (stedents and search).


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.disconnect()
    return response


@app.route('/')
def index():
    discipline = db.get_table('discipline')
    student = db.get_table('student')
    return render_template(
        'home.html', students=student.count(), disciplines=discipline.count()
    )


@app.route('/discipline', methods=['GET', 'POST'])
def discipline():
    """
    View for all disciplines.
    """
    discipline = db.get_table('discipline')
    disciplines = discipline.get()
    form = DisciplineForm()
    if form.validate_on_submit():
        discipline.add(form.title.data)
        return redirect(url_for('discipline'))
    return render_template(
        'discipline.html', disciplines=disciplines, form=form
    )


@app.route('/discipline/<int:identificator>', methods=['DELETE'])
def del_discipline(identificator):
    discipline = db.get_table('discipline')
    discipline.remove(identificator)
    return redirect(url_for('discipline'))


@app.route('/discipline/<int:identificator>', methods=['PUT'])
def update_discipline(identificator):
    new_title = request.args.get('title')
    if new_title:
        discipline = db.get_table('discipline')
        discipline.update(identificator, new_title)
    return redirect(url_for('discipline'))


@app.route('/student', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route(
    '/student/page/<int:page>', methods=['GET', 'POST']
)
def students(page):
    """
    View for all students.
    """
    student = db.get_table('student')
    total = student.count()
    paginator = Paginator(page, PER_PAGE, total)
    offset = None if page == 1 else PER_PAGE * paginator.previous
    students = student.get(offset=offset, limit=PER_PAGE)
    form = StudentForm()
    if form.validate_on_submit():
        student.add(form.name.data)
        return redirect(url_for('students'))
    return render_template(
        'students.html', students=students,
        form=form, paginator=paginator
    )

@app.route(
    '/search', defaults={'page': 1, 'query': None}, methods=['GET', 'POST']
)
@app.route('/search/page/<int:page>/<query>', methods=['GET', 'POST'])
def search(page, query, paginator=None, students=None, offset=None):
    """
    View for students search.
    """
    form = SearchForm()
    if form.validate_on_submit():
        student = db.get_table('student')
        total = student.count(form.name.data)
        page = 1
        paginator = Paginator(page, PER_PAGE, total)
        students = student.search(form.name.data, offset, PER_PAGE)
        query = form.name.data
    elif query is not None:
        student = db.get_table('student')
        total = student.count(query)
        paginator = Paginator(page, PER_PAGE, total)
        if page != 1:
            offset = PER_PAGE * paginator.previous
        students = student.search(query, offset, PER_PAGE)
    return render_template(
        'search.html', students=students,
        form=form, paginator=paginator, query=query
    )


@app.route('/student/<int:identificator>', methods=['GET', 'POST'])
def student(identificator):
    """
    View for student card.
    """
    student_table = db.get_table('student')
    student = student_table.get(identificator)
    if student is None:
        abort(404)
    discipline = db.get_table('discipline')
    disciplines = discipline.get()
    scores = student_table.get_scores(identificator)
    for each in disciplines:
        if each['id'] not in scores:
            scores[each['id']] = {'score': '', 'id': 0}
    form = StudentForm()
    return render_template(
        'student.html', student=student,
        form=form, disciplines=disciplines,
        scores=scores
    )


@app.route('/student/<int:identificator>', methods=['DELETE'])
def del_student(identificator):
    student = db.get_table('student')
    student.remove(identificator)
    return redirect(url_for('students'))


@app.route('/student/<int:identificator>', methods=['PUT'])
def update_student(identificator):
    new_name = request.args.get('name')
    if new_name:
        student = db.get_table('student')
        student.update(identificator, new_name)
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
        except ValueError:
            # Check that incoming data are valid.
            pass
    return redirect(url_for('student', identificator=identificator))


@app.route('/student/<int:identificator>/<int:score_id>/', methods=['PATCH'])
def unset_score(identificator, score_id):
    student = db.get_table('student')
    student.unset_score(score_id)
    return redirect(url_for('student', identificator=identificator))
