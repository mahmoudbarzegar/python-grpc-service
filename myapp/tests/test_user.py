from django.test import TestCase
from django.contrib.auth import get_user_model


# from django.contrib.auth.models import User

class UserTestClass(TestCase):

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='testuser@example.com',
            password='password123'
        )

    def test_user_creation(self):
        # Verify that user was created
        self.assertEquals(self.user.username, 'test_user')
        self.assertEquals(self.user.email, 'testuser@example.com')

    def test_user_authentication(self):
        # Test that the user can be authenticated
        user = get_user_model().objects.get(username='test_user')
        self.assertTrue(user.check_password('password123'))

    def test_user_is_active(self):
        # Verify that the user is active
        self.assertTrue(self.user.is_active)

    def test_user_is_not_staff(self):
        # Verify that the user is not staff by default
        self.assertFalse(self.user.is_staff)

    def test_user_is_not_superuser(self):
        # Verify that the user is not a superuser by default
        self.assertFalse(self.user.is_superuser)