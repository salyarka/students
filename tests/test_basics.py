import unittest
from flask import current_app
from app import app


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object('app.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])