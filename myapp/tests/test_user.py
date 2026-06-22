from django.test import TestCase


class UserTestClass(TestCase):
    def test_user_creation(self):
        """Test POST request."""
        response = self.client.post(
            "/myapp/create-user/",
            data={"username": "mahmoud-twm-2026", "email": "mahmodud-twm-2026@local.com", "password": "1236549"},
            format="json",
            content_type="application/json",  # Explicitly set
        )

        # Check status code
        self.assertEqual(response.status_code, 201)
