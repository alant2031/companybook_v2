import random
import pytest
import os

# from unittest import skip
from django.test import TestCase
from django.utils.text import slugify
from model_bakery import baker
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from . import phones, docs, usernames

from core.models import PhoneField, DocumentField, UsernameField


@pytest.mark.mo
class PhoneFieldTestCase(TestCase):
    def setUp(self):
        self.field = PhoneField()
        self.invalid_phones = [
            "(01)988887777",
            "8abc345999999",
            "(12)144445555",
            "(12)444444",
            "(12)9888877771",
        ]

        self.valid_phone = random.choice(phones)

    def test_valid_phone_number(self):
        value = self.field.clean(self.valid_phone, None)

        self.assertEqual(value, self.valid_phone)

    def test_invalid_phone_number(self):
        for invalid_phone in self.invalid_phones:
            with self.assertRaises(ValidationError):
                self.field.clean(invalid_phone, None)


@pytest.mark.mo
class UsernameFieldTestCase(TestCase):
    def setUp(self):
        self.field = UsernameField()
        self.invalid_usernames = [
            "@johndoe",
            "Johndoeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "_jane",
            "_",
            "12",
            "12jane",
            "jan",
        ]

        self.valid_username = random.choice(usernames)

    def test_valid_username(self):
        value = self.field.clean(self.valid_username, None)

        self.assertEqual(value, self.valid_username)

    def test_invalid_username(self):
        for invalid_username in self.invalid_usernames:
            with self.assertRaises(ValidationError):
                self.field.clean(invalid_username, None)


@pytest.mark.mo
class DocumentFieldTestCase(TestCase):
    def setUp(self):
        self.field = DocumentField()
        self.valid_doc = random.choice(docs)
        self.invalid_docs = [
            "26.005.330/0001-63",
            "qwertyughijnbf",
        ]

    def test_valid_doc(self):
        value = self.field.clean(self.valid_doc, None)
        self.assertEqual(self.valid_doc, value)

    def test_invalid_doc(self):
        for invalid_doc in self.invalid_docs:
            with self.assertRaises(ValidationError):
                self.field.clean(invalid_doc, None)


@pytest.mark.mo
class CompanyTestCase(TestCase):
    def setUp(self):
        self.company = baker.make("Company")
        self.cnpj = "36088273000187"

    def test_str(self):
        self.assertEqual(str(self.company), self.company.razao[:30])

    def test_unique_document(self):
        with self.assertRaises(IntegrityError):
            baker.make("Company", document="19726674000135")
            baker.make("Company", document="19726674000135")

    def test_is_cpf(self):
        with self.assertRaises(ValidationError):
            c1 = baker.make("Company", document="79207516080")
            c1.clean()
        with self.assertRaises(ValidationError):
            c2 = baker.make("Company", document="49726674000135", is_cpf=True)
            c2.clean()

    def test_clean_method(self):
        try:
            c3 = baker.make("Company", document=self.cnpj)
            c3.clean()
        except Exception as e:
            self.fail(f"An error occurred while creating the object: {e}")


@pytest.mark.mo
class SubscriberTestCase(TestCase):
    def setUp(self):
        self.tekno = baker.make_recipe("core.tests.subscriber_tekno")

    def test_str(self):
        self.assertEqual(
            str(self.tekno), f"Assinante {self.tekno.company.name[:30]}"
        )

    def test_unique_company(self):
        with self.assertRaises(IntegrityError):
            company = baker.make("Company", document="19226674000135")
            baker.make("Subscriber", company=company, username="mashala44")
            baker.make("Subscriber", company=company, username="mashala55")

    def test_unique_username(self):
        with self.assertRaises(IntegrityError):
            c1 = baker.make("Company", document="19946674000135")
            c2 = baker.make("Company", document="19536674000182")
            baker.make("Subscriber", company=c1, username="mashala99")
            baker.make("Subscriber", company=c2, username="mashala99")

    def test_path_logo(self):
        pk = str(self.tekno.company.pk)
        slug = slugify(self.tekno.company.razao)
        pathname = os.path.join(pk, f"{slug}-logo.jpg")

        self.assertEqual(str(self.tekno.logo), pathname)

    def test_path_photos(self):
        pk = str(self.tekno.company.pk)
        slug = slugify(self.tekno.company.razao)
        for i in range(4):
            key = "photo" + str(i + 1)
            pathname = os.path.join(pk, f"{slug}-{key}.jpg")
            photo_attr = getattr(self.tekno, key)
            self.assertEqual(str(photo_attr), pathname)


@pytest.mark.mo
class CategoryTestCase(TestCase):
    def test_str(self):
        category = baker.make("Category")
        self.assertEqual(str(category), category.name)
