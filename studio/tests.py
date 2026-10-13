from django.test import TestCase

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
        self.assertEqual(len(response.context["apparel_products"]), 10)
        for category in ("sports-bras", "bodysuits", "leggings", "sports-tops", "matching-sets"):
            self.assertContains(response, f'data-filter="{category}"')
        self.assertContains(response, "cdn.shopify.com")
        self.assertContains(response, "bombshellsportswear.com")

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