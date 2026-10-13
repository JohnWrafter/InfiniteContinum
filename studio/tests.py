from django.test import TestCase
from django.contrib.staticfiles import finders

from studio.models import MemberInquiry


class HomePageTests(TestCase):
    def test_homepage_displays_default_strength_plan(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Infinite Continuum")
        self.assertContains(response, "Build strength")
        self.assertContains(response, "Full-body foundations")

    def test_plan_can_be_personalized(self):
        response = self.client.get("/", {"focus": "mobility", "sessions": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Move with more ease")
        self.assertContains(response, "Space to move")
        self.assertNotContains(response, "Reset and restore")

    def test_apparel_section_covers_requested_categories_and_source(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["apparel_products"]), 42)
        for category in ("sports-bras", "bodysuits", "leggings", "sports-tops", "matching-sets"):
            self.assertContains(response, f'data-filter="{category}"')
        self.assertContains(response, "/static/Sports-Bras/")
        self.assertContains(response, "bombshellsportswear.com")

    def test_apparel_cards_use_local_images_gbp_prices_descriptions_and_sizes(self):
        response = self.client.get("/")
        products = response.context["apparel_products"]

        self.assertEqual(products[0]["image"], "Sports-Bras/contrast-voltage-hollywood-pink.jpg")
        self.assertIsNotNone(finders.find(products[0]["image"]))
        self.assertContains(response, "£65")
        self.assertContains(response, "£162")
        self.assertContains(response, "UK PRICES IN GBP")
        self.assertContains(response, "Contrast trim, adjustable straps")
        self.assertContains(response, "43609887309911")
        self.assertContains(response, "Shop Leggings")
        self.assertContains(response, "Shop Sports bra")

    def test_every_sports_bra_image_has_a_local_product_card(self):
        response = self.client.get("/")
        image_edits = [
            product
            for product in response.context["apparel_products"]
            if product.get("collection_only") and product["category"] == "sports-bras"
        ]

        self.assertEqual(len(image_edits), 16)
        for product in image_edits:
            with self.subTest(image=product["image"]):
                self.assertIsNotNone(finders.find(product["image"]))
                self.assertContains(response, product["image"])
                self.assertContains(response, "From £59")
                self.assertContains(response, "data-size-mode=\"collection\"")

    def test_every_unique_local_leggings_image_has_a_product_card(self):
        response = self.client.get("/")
        leggings_edits = [
            product
            for product in response.context["apparel_products"]
            if product.get("collection_only") and product["category"] == "leggings"
        ]

        self.assertEqual(len(leggings_edits), 16)
        for product in leggings_edits:
            with self.subTest(image=product["image"]):
                self.assertIsNotNone(finders.find(product["image"]))
                self.assertContains(response, product["image"])
                self.assertContains(response, "From £93")
                self.assertContains(response, product["description"])
                self.assertContains(response, product["url"])

    def test_invalid_plan_parameters_fall_back_safely(self):
        response = self.client.get("/", {"focus": "unknown", "sessions": "99"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Full-body foundations")

    def test_valid_membership_enquiry_is_saved(self):
        response = self.client.post(
            "/",
            {"name": "Jordan Lee", "email": "jordan@example.com", "focus": "endurance"},
        )
        self.assertRedirects(response, "/")
        self.assertEqual(MemberInquiry.objects.count(), 1)
        self.assertEqual(MemberInquiry.objects.get().focus, "endurance")

    def test_invalid_membership_enquiry_is_not_saved(self):
        response = self.client.post(
            "/",
            {"name": "Jordan Lee", "email": "not-an-email", "focus": "strength"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MemberInquiry.objects.count(), 0)