import psycopg2
from psycopg2.extras import DictCursor


class Table:
    """Abstract class Table
    Describes common actions with tables.
    """
    def __init__(self, conn, cur, validator):
        self.conn = conn
        self.cur = cur
        self.validator = validator

    def get(self):
        raise NotImplementedError('Subclasses should implement this!')

    def add(self):
        raise NotImplementedError('Subclasses should implement this!')

    def remove(self):
        raise NotImplementedError('Subclasses should implement this!')

    def update(self):
        raise NotImplementedError('Subclasses should implement this!')

    def count(self):
        raise NotImplementedError('Subclasses should implement this!')


class Student(Table):
    """
    Implements the work with the table student.
    """

    def get(self, identificator=None, offset=None, limit=15):
        dict_cur = self.conn.cursor(cursor_factory=DictCursor)
        if identificator is None:
            dict_cur.execute(
                'SELECT id, name FROM student '
                'ORDER BY id DESC OFFSET %s LIMIT %s;',
                (offset, limit)
            )
            return [dict(row) for row in dict_cur]
        dict_cur.execute(
            'SELECT id, name FROM student WHERE id = %s;',
            (identificator,)
        )
        return dict_cur.fetchone()

    def add(self, name):
        self.cur.execute(
            'INSERT INTO student(name) VALUES (%s);',
            (name,)
        )

    def remove(self, identificator):
        if self.validator.int_col(identificator):
            self.cur.execute(
                'DELETE FROM student WHERE id = %s;', (identificator,)
            )

    def update(self, identificator, name):
        self.cur.execute(
            'UPDATE student SET name = %s WHERE id = %s;',
            (name, identificator)
        )

    def count(self, string=None):
        if string is None:
            self.cur.execute('SELECT count(id) FROM student;')
        else:
            self.cur.execute(
                'SELECT count(id) FROM student WHERE name LIKE %s;',
                ('%{}%'.format(string),)
            )
        return self.cur.fetchone()[0] 

    def get_scores(self, identificator):
        if self.validator.int_col(identificator):
            dict_cur = self.conn.cursor(cursor_factory=DictCursor)
            dict_cur.execute(
                'SELECT id, discipline_id, score '
                'FROM student_discipline WHERE student_id = %s;',
                (identificator,)
            )
            return {
                dict(row)['discipline_id']: {
                    'score': dict(row)['score'], 'id': dict(row)['id']
                } for row in dict_cur
            }

    def set_score(self, new_score, discipline, student_id, score_id):
        if not score_id:
            self.cur.execute(
                'INSERT INTO student_discipline '
                '(score, discipline_id, student_id) VALUES (%s, %s, %s);',
                (new_score, discipline, student_id)
            )
        else:
            self.cur.execute(
                'UPDATE student_discipline SET score = %s WHERE id = %s;',
                (new_score, score_id)
            )

    def unset_score(self, score_id):
        if self.validator.int_col(score_id):
            self.cur.execute(
                'DELETE FROM student_discipline WHERE id = %s;', (score_id,)
            )

    def search(self, string, offset, limit):
        dict_cur = self.conn.cursor(cursor_factory=DictCursor)
        dict_cur.execute(
            'SELECT id, name FROM student WHERE'
            ' name LIKE %s OFFSET %s LIMIT %s;',
            ('%{}%'.format(string), offset, limit)
        )
        return [dict(row) for row in dict_cur]


class Discipline(Table):
    """
    Implements the work with the table discipline.
    """

    def add(self, title):
        if self.validator.text_col(title):
            self.cur.execute(
                'INSERT INTO discipline(title) VALUES (%s);', (title,)
            )

    def get(self):
        dict_cur = self.conn.cursor(cursor_factory=DictCursor)
        dict_cur.execute('SELECT id, title FROM discipline')
        return [dict(row) for row in dict_cur]

    def remove(self, identificator):
        if self.validator.int_col(identificator):
            self.cur.execute(
                'DELETE FROM discipline WHERE id = %s;', (identificator,)
            )

    def update(self, identificator, title):
        if self.validator.int_col(identificator) and \
        self.validator.text_col(title):
            self.cur.execute(
                'UPDATE discipline SET title = %s WHERE id = %s;',
                (title, identificator)
            )

    def count(self):
        self.cur.execute('SELECT count(id) FROM discipline;')
        return self.cur.fetchone()[0]


class Validator:

    def __init__(self, max_length):
        self.max_length = max_length

    def text_col(self, data):
        return len(data) <= self.max_length

    def int_col(self, data):
        try:
            return int(data)
        except ValueError:
            pass


class DB:
    """
    Implements connection with database,
    and creation of objects which work with tables
    """
    tables = {
        'student': {'model': Student, 'max_length': 40},
        'discipline': {'model': Discipline, 'max_length': 40}
    }

    def __init__(self, app):
        self.credentials = app.config['DATABASE']

    def execute_sql(self, source):
        self.connect()
        with open(source, mode='r') as f:
            self.cur.execute(f.read())
        self.disconnect()

    def connect(self):
        self.conn = psycopg2.connect(**self.credentials)
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_table(self, table_name):
        table = self.tables.get(table_name)
        if table is not None:
            return table['model'](
                self.conn, self.cur, Validator(table['max_length'])
            )
