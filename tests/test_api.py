import os

os.environ['TEST_ENV'] = 'true'

from app.api import app, db
from app.models import Package, PostOffice
from unittest import TestCase


class TestApiIndex(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        # When
        response = self.client.get('/')

        # Then
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"Cellosign - Gil Halperin", response.data)


class TestApiPackage(TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_register__no_params_error(self):
        # When
        response = self.client.post('/package/register')

        # Then
        self.assertEquals(response.status_code, 400)

    def test_register(self):
        # When
        response = self.client.post('/package/register', data={"recipient_name": "RES", "destination_address": "ADD",
                                                               "destination_zip_code": "ZIP", "package_type": "LETTER"})
        package = Package.query.first()

        # Then
        self.assertEquals(response.status_code, 201)
        self.assertEquals(package.package_type.value, "Letter")
        self.assertEquals(package.delivered, False)
        self.assertEquals(package.destination_zip_code, "ZIP")
        self.assertEquals(package.destination_address, "ADD")


class TestApiOffice(TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_creation(self):
        # When
        response = self.client.post('/office', data={"name": "NAME", "address": "ADD", "zip_code": "ZIP"})

        # Then
        self.assertEquals(response.status_code, 201)

        post_office = PostOffice.query.first()
        self.assertEquals(post_office.name, "NAME")
        self.assertEquals(post_office.zip_code, "ZIP")
        self.assertEquals(post_office.address, "ADD")
