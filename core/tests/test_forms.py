from django.test import TestCase
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from core.forms import SubscriberForm
import copy
import pytest
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIRED_FIELD_MESSAGE = "Este campo é obrigatório."


@pytest.mark.fo
class SubscriberFormTestCase(TestCase):
    def setUp(self):
        logo_image_path = os.path.join(BASE_DIR, "imgs", "logo.png")
        photo_image_path = os.path.join(BASE_DIR, "imgs", "photo.png")
        big_image_path = os.path.join(BASE_DIR, "imgs", "big.png")
        with open(logo_image_path, "rb") as f:
            self.logo_png = f.read()
        with open(photo_image_path, "rb") as f:
            self.photo_png = f.read()
        with open(big_image_path, "rb") as f:
            self.big_png = f.read()
        self.form = SubscriberForm
        self.user = baker.make("User")
        self.company1 = baker.make("Company", document="54408794000157")
        self.company2 = baker.make("Company", document="54408794000156")
        self.data = {
            "user": self.user,
            "company": self.company1,
            "in_charge": "Marty",
            "username": "marty_mcfly",
            "opening_h": "8h-16h",
            "opening_d": datetime.now(),
            "wpp": "https://example.com/",
            "instagram": "https://example.com/",
            "facebook": "https://example.com/",
            "website": "https://example.com/",
            "iframe": "<iframe src='https://example.com/' width='600' height='450'></iframe>",  # noqa
            "obs": "That is for messing",
        }

    def test_valid_form(self):
        d = copy.deepcopy(self.data)
        logo_dict = {
            "logo": SimpleUploadedFile(
                name="pic.png",
                content=self.logo_png,
                content_type="image/png",
            )
        }
        photos_dict = {
            "photo"
            + str(i + 1): SimpleUploadedFile(
                name=f"p{i+1}.png",
                content=self.photo_png,
                content_type="image/png",
            )
            for i in range(4)
        }
        d.update(logo_dict)
        d.update(photos_dict)
        f = self.form(
            data=d,
            files=d,
        )
        for field_name, errors in f.errors.items():
            print(f"Field: {field_name}, Error: {', '.join(errors)}")
        self.assertTrue(f.is_valid())

    def test_company_is_required(self):
        d = copy.deepcopy(self.data)
        d["company"] = None
        f = self.form(
            data=d,
            files={
                "logo": SimpleUploadedFile(
                    name="pic.png",
                    content=self.logo_png,
                    content_type="image/png",
                )
            },
        )
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors["company"][0],
            REQUIRED_FIELD_MESSAGE,
        )

    def test_in_charge_is_required(self):
        d = copy.deepcopy(self.data)
        d["in_charge"] = None
        f = self.form(
            data=d,
            files={
                "logo": SimpleUploadedFile(
                    name="pic.png",
                    content=self.logo_png,
                    content_type="image/png",
                )
            },
        )
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors["in_charge"][0],
            REQUIRED_FIELD_MESSAGE,
        )

    def test_username_is_required(self):
        d = copy.deepcopy(self.data)
        d["username"] = None
        f = self.form(
            data=d,
            files={
                "logo": SimpleUploadedFile(
                    name="pic.png",
                    content=self.logo_png,
                    content_type="image/png",
                )
            },
        )
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors["username"][0],
            REQUIRED_FIELD_MESSAGE,
        )

    def test_logo_is_required(self):
        d = copy.deepcopy(self.data)
        f = self.form(
            data=d,
        )
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors["logo"][0],
            REQUIRED_FIELD_MESSAGE,
        )

    def test_logo_is_larger_than_200kb(self):
        f = self.form(
            data=self.data,
            files={
                "logo": SimpleUploadedFile(
                    name="pic.png",
                    content=self.big_png,
                    content_type="image/png",
                )
            },
        )
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors["logo"][0],
            "The image size exceeds the maximum allowed size of 200KB.",
        )

    def test_photo_is_larger_than_500kb(self):
        f = self.form(
            data=self.data,
            files={
                "logo": SimpleUploadedFile(
                    name="pic.png",
                    content=self.logo_png,
                    content_type="image/png",
                ),
                "photo1": SimpleUploadedFile(
                    name="p1.png",
                    content=self.big_png,
                    content_type="image/png",
                ),
            },
        )
        self.assertFalse(f.is_valid())
        self.assertEqual(
            f.errors["photo1"][0],
            "The image size exceeds the maximum allowed size of 500KB.",
        )
