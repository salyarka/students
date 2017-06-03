from app import app
from flask_script import Manager


manager = Manager(app)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def init_db():
    from app.db import DB
    db = DB(app)
    db.init_db()
    print('Database initialized.')


if __name__ == '__main__':
    manager.run()
