import psycopg2

class DB:

    def __init__(self, app):
        self.conn = psycopg2.connect(**app.config['DATABASE'])
        self.cur = self.conn.cursor()