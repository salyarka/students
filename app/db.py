import psycopg2
from psycopg2.extras import DictCursor


class Table:

    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

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

    def get(self, identificator=None, offset=None, limit=5):
        dict_cur = self.conn.cursor(cursor_factory=DictCursor)
        if identificator is None:
            dict_cur.execute(
                'SELECT id, name, surname FROM student '
                'ORDER BY id OFFSET %s LIMIT %s;',
                (offset, limit)
            )
            return [dict(row) for row in dict_cur]
        dict_cur.execute(
            'SELECT id, name, surname FROM student WHERE id = %s;',
            (identificator,)
        )
        return dict_cur.fetchone()

    def add(self, name, surname):
        self.cur.execute(
            'INSERT INTO student(name, surname) VALUES (%s, %s);',
            (name, surname)
        )

    def remove(self, identificator):
        self.cur.execute(
            'DELETE FROM student WHERE id = %s;', (identificator,)
        )

    def update(self, identificator, name, surname):
        self.cur.execute(
            'UPDATE student SET name = %s, surname = %s WHERE id = %s;',
            (name, surname, identificator)
        )

    def count(self):
        self.cur.execute('SELECT count(id) FROM student;')
        return self.cur.fetchone()[0]

    def get_scores(self, identificator):
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
        self.cur.execute(
            'DELETE FROM student_discipline WHERE id = %s;', (score_id,)
        )

    # def search(self, string):
    #     return self.cur.execute(
    #         'SELECT id FROM student WHERE name LIKE "%%s%" or surname LIKE "%%s%";',
    #         (string, string)
    #     )


class Discipline(Table):

    def add(self, title):
        self.cur.execute(
            'INSERT INTO discipline(title) VALUES (%s);', (title,)
        )

    def get(self):
        dict_cur = self.conn.cursor(cursor_factory=DictCursor)
        dict_cur.execute('SELECT id, title FROM discipline')
        return [dict(row) for row in dict_cur]

    def remove(self, identificator):
        self.cur.execute(
            'DELETE FROM discipline WHERE id = %s;', (identificator,)
        )

    def update(self, identificator, title):
        self.cur.execute(
            'UPDATE discipline SET title = %s WHERE id = %s;',
            (title, identificator)
        )

    def count(self):
        self.cur.execute('SELECT count(id) FROM discipline;')
        return self.cur.fetchone()[0]


class DB:
    tables = {
        'student': Student,
        'discipline': Discipline
    }

    def __init__(self, app):
        # self.app = app
        self.credentials = app.config['DATABASE']
        # self.conn = psycopg2.connect(**app.config['DATABASE'])
        # self.cur = self.conn.cursor()

    def init_db(self):
        self.connect()
        with open('schema.sql', mode='r') as f:
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
            # return table(self.conn, self.cur)
            return table(self.conn, self.cur)

    # def commit(self):
    #     self.conn.commit()
        