import unittest
from src import app


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass


class AppTestCase(BaseTestCase):
    def setUp(self) -> None:
        super(AppTestCase, self).setUp()
        self.client = app.test_client(self)

    def test_app(self):
        pass
