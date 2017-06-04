import psycopg2
import psycopg2.extras

class DB:

    def __init__(self, app):
        self.conn = psycopg2.connect(**app.config['DATABASE'])
        self.cur = self.conn.cursor()

    def init_db(self):
        with open('schema.sql', mode='r') as f:
            self.cur.execute(f.read())
            self.conn.commit()

    def get_model(self, model_name):
        if model_name == 'Student':
            return Student(self.conn, self.cur)
        elif model_name == 'Discipline':
            return Discipline(self.conn, self.cur)

    def commit(self):
        self.conn.commit()


class Student:

    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def get(self):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT id, name, surname FROM student')
        return [dict(row) for row in dict_cur]

    def add(self, name, surname):
        self.cur.execute(
            'INSERT INTO student(name, surname) VALUES (%s, %s);',
            (name, surname)
        )

    def remove(self, identificator):
        self.cur.execute(
            'DELETE FROM student WHERE id = %s;', (identificator,)
        )

    def update_row(self, name, surname, identificator):
        self.cur.execute(
            'UPDATE student SET name = %s, surname = %s WHERE id = %s;',
            (name, surname, identificator)
        )

class Discipline:

    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def add(self, title):
        self.cur.execute(
            'INSERT INTO discipline(title) VALUES (%s);', (title,)
        )

    def get(self):
        dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute('SELECT id, title FROM discipline')
        return [dict(row) for row in dict_cur]

    def remove(self, identificator):
        self.cur.execute(
            'DELETE FROM discipline WHERE id = %s;', (identificator,)
        )

    def update_row(self, title, identificator):
        self.cur.execute(
            'UPDATE discipline SET title = %s WHERE id = %s;',
            (title, identificator)
        )
