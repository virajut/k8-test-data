import unittest
from src import create_app


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app()
        self.client = app.test_client(self)

    def tearDown(self) -> None:
        pass
