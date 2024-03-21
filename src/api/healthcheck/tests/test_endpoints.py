import unittest

from fastapi import status
from fastapi.testclient import TestClient

from core.settings import settings
from main import app


class TestHelathcheckEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_healthcheck(self):
        url = "/health-check"
        response = self.client.get(url)

        body = response.json().get("body")
        expected_keys = ["detail", "version"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)
        self.assertEqual(body.get("detail"), settings.PROJECT_NAME)
        self.assertEqual(body.get("version"), settings.VERSION)
