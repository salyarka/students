from flask_script import Manager
from app import app


manager = Manager(app)
commands = {
    'init': 'schema.sql',
    'fill': 'fill.sql'
}

@manager.command
def test():
    """Command to run tests
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def db(action):
    """Command for db management
    Start command if exist, otherwise prints available commands in console.
    """
    if action not in commands:
        return 'Available commands: %s' % list(commands.keys())
    from app.db import DB
    db = DB(app)
    db.execute_sql(commands[action])
    return 'Database %sed' % action


if __name__ == '__main__':
    manager.run()
