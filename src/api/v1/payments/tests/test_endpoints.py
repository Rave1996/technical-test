import unittest
import os

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from core.settings import settings
from main import app
from db.utils import populate_db
from db.models.base import Base
from db.session import engine


class TestCustomersEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

        Base.metadata.create_all(engine)

        # Fill DB with data
        populate_db(engine)

    def test_loans_retrieve(self):
        url = "/v1/loans/retrieve/2"

        response = self.client.get(url)

        body = response.json().get("body")
        expected_keys = ["id", "customer_id", "amount", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 2)
        self.assertEqual(body.get("customer_id"), 1)
        self.assertEqual(body.get("amount"), 8683.0)
        self.assertTrue(body.get("status"))

    def test_loans_create(self):
        url = "/v1/loans/create"

        json_data = {
            "customer_id": 3,
            "amount": 1000
        }

        response = self.client.post(url, json=json_data)

        body = response.json().get("body")
        expected_keys = ["id", "customer_id", "amount", "status"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertIsInstance(body.get("id"), int)
        self.assertEqual(body.get("customer_id"), 3)
        self.assertEqual(body.get("amount"), 1000.0)
        self.assertEqual(body.get("status"), True)

    def test_loans_delete(self):
        url = "/v1/loans/delete/6"

        response = self.client.delete(url)

        body = response.json().get("body")
        expected_keys = ["id", "customer_id", "amount", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 6)
        self.assertEqual(body.get("customer_id"), 2)
        self.assertEqual(body.get("amount"), 7543.0)
        self.assertEqual(body.get("status"), True)

    def test_loans_disable(self):
        url = "/v1/loans/disable/7"

        response = self.client.delete(url)

        body = response.json().get("body")
        expected_keys = ["id", "customer_id", "amount", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 7)
        self.assertEqual(body.get("customer_id"), 3)
        self.assertEqual(body.get("amount"), 6752.0)
        self.assertEqual(body.get("status"), False)

    def test_loans_enable(self):
        url = "/v1/loans/enable/7"

        response = self.client.patch(url)

        body = response.json().get("body")
        expected_keys = ["id", "customer_id", "amount", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 7)
        self.assertEqual(body.get("customer_id"), 3)
        self.assertEqual(body.get("amount"), 6752.0)
        self.assertEqual(body.get("status"), True)