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

    def test_customer_retrieve(self):
        url = "/v1/customers/retrieve/2"

        response = self.client.get(url)

        body = response.json().get("body")
        expected_keys = ["id", "full_name", "email", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 2)
        self.assertEqual(body.get("full_name"), "Maria Rodriguez")
        self.assertEqual(body.get("email"), "maria@email.com")
        self.assertEqual(body.get("status"), True)

    def test_customer_create(self):
        url = "/v1/customers/create"

        json_data = {
            "full_name": "John Doe",
            "email": "JohnDoe@email.com"
        }

        response = self.client.post(url, json=json_data)

        body = response.json().get("body")
        expected_keys = ["id", "full_name", "email", "status"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertIsInstance(body.get("id"), int)
        self.assertEqual(body.get("full_name"), "John Doe")
        self.assertEqual(body.get("email"), "JohnDoe@email.com")
        self.assertEqual(body.get("status"), True)

    def test_customer_delete(self):
        url = "/v1/customers/delete/1"

        response = self.client.delete(url)

        body = response.json().get("body")
        expected_keys = ["id", "full_name", "email", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 1)
        self.assertEqual(body.get("full_name"), "Juan Perez")
        self.assertEqual(body.get("email"), "juan@email.com")
        self.assertEqual(body.get("status"), False)

    def test_customer_disable(self):
        url = "/v1/customers/disable/2"

        response = self.client.delete(url)

        body = response.json().get("body")
        expected_keys = ["id", "full_name", "email", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 2)
        self.assertEqual(body.get("full_name"), "Maria Rodriguez")
        self.assertEqual(body.get("email"), "maria@email.com")
        self.assertEqual(body.get("status"), False)

    def test_customer_enable(self):
        url = "/v1/customers/enable/2"

        response = self.client.patch(url)

        body = response.json().get("body")
        expected_keys = ["id", "full_name", "email", "status"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)

        self.assertEqual(body.get("id"), 2)
        self.assertEqual(body.get("full_name"), "Maria Rodriguez")
        self.assertEqual(body.get("email"), "maria@email.com")
        self.assertEqual(body.get("status"), True)