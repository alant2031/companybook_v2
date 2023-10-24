import pytest

# from unittest import skip
from django.test import TestCase
from model_bakery import baker

from django.urls import reverse


@pytest.mark.vi
class IndexViewTestCase(TestCase):
    def setUp(self):
        for i in range(5):
            subscriber = baker.make_recipe("core.tests.subscriber_view")
            if i == 0:
                subscriber.active = False
                subscriber.save()

        self.response = self.client.get(reverse("subs"))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_active_subscribers(self):
        subs = self.response.context["subs"]
        self.assertIs(len(subs), 4)
        self.assertTrue(all(sub.active for sub in subs))


@pytest.mark.vi
class SubscriberSearchViewTestCase(TestCase):
    def setUp(self):
        self.game_category = baker.make("Category", name="GAME")
        self.book_category = baker.make("Category", name="BOOK")
        for i in range(5):
            id = str(i + 1)
            ctg = self.book_category if i % 2 == 0 else self.game_category
            if i > 1:
                company_A = baker.make(
                    "Company",
                    name="PAULA FERNANDES",
                    document="1780802800010" + id,
                    categoria1=ctg,
                    uf="PA",
                )
                baker.make(
                    "Subscriber", company=company_A, username=f"fernandes{id}"
                )
            else:
                company_B = baker.make(
                    "Company",
                    name="PAULA ROBERTA",
                    document="1780802800010" + id,
                    categoria1=ctg,
                    uf="BA",
                )
                baker.make(
                    "Subscriber", company=company_B, username=f"roberta{id}"
                )

    def test_status_code(self):
        response = self.client.get(
            reverse("search"),
            {"location": "n", "category": "t", "search_term": ""},
        )
        self.assertEqual(response.status_code, 200)

    def test_search_term(self):
        search_term = "ROBERTA"
        response = self.client.get(
            reverse("search"),
            {"location": "n", "category": "t", "search_term": search_term},
        )
        subs = response.context["subs"]
        self.assertTrue(all(sub.active for sub in subs))
        self.assertTrue(all(search_term in sub.company.name for sub in subs))
        self.assertIs(len(subs), 2)

    def test_search_category(self):
        category = self.book_category
        response = self.client.get(
            reverse("search"),
            {
                "location": "n",
                "search_term": "",
                "category": category.pk,
            },
        )
        subs = response.context["subs"]
        self.assertTrue(all(sub.active for sub in subs))
        self.assertIs(len(subs), 3)

    def test_search_location(self):
        local = "BA"
        response = self.client.get(
            reverse("search"),
            {
                "location": local,
                "search_term": "",
                "category": "t",
            },
        )
        subs = response.context["subs"]
        self.assertTrue(all(sub.active for sub in subs))
        self.assertTrue(all((local in sub.company.uf) for sub in subs))
        self.assertIs(len(subs), 2)

    def test_search_multiparams(self):
        local = "PA"
        ctg_id = self.book_category.id
        response = self.client.get(
            reverse("search"),
            {"location": local, "search_term": "", "category": ctg_id},
        )
        subs = response.context["subs"]
        self.assertTrue(all(sub.active for sub in subs))
        self.assertTrue(all((local in sub.company.uf) for sub in subs))
        self.assertIs(len(subs), 2)


@pytest.mark.vi
class SubscriberViewTestCase(TestCase):
    def setUp(self):
        self.active_subscriber = baker.make_recipe(
            "core.tests.subscriber_view"
        )
        self.inactive_subscriber = baker.make_recipe(
            "core.tests.subscriber_view"
        )
        self.inactive_subscriber.active = False
        self.inactive_subscriber.save()
        self.random_username = "axznt67"
        self.company_name = self.active_subscriber.company.name
        self.company_category = self.active_subscriber.company.categoria1
        self.sub_logo = self.active_subscriber.logo

    def test_status_code(self):
        response = self.client.get(
            reverse(
                "details", kwargs={"username": self.active_subscriber.username}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_404_not_found(self):
        resp_random_username = self.client.get(
            reverse("details", kwargs={"username": self.random_username})
        )
        resp_inactive_subscriber = self.client.get(
            reverse(
                "details",
                kwargs={"username": self.inactive_subscriber.username},
            )
        )
        self.assertEqual(resp_random_username.status_code, 404)
        self.assertEqual(resp_inactive_subscriber.status_code, 404)

    def test_subscriber_details(self):
        response = self.client.get(
            reverse(
                "details", kwargs={"username": self.active_subscriber.username}
            )
        )
        sub = response.context["sub"]
        name = sub.company.name
        category = sub.company.categoria1
        logo = sub.logo

        self.assertTrue(sub.active)
        self.assertEqual(self.company_name, name)
        self.assertEqual(self.company_category, category)
        self.assertEqual(self.sub_logo, logo)
