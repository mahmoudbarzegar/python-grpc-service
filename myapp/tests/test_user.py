from django.test import TestCase

class UserTestClass(TestCase):

    def test_user_creation(self):
        """Test POST request """
        response = self.client.post('/myapp/create-user/',
            data={
                "username": "Mark",
                "email": "mark@local",
                "password": "123654"
            }, 
            format='json',
            content_type='application/json'  # Explicitly set
        )

         # Check status code
        self.assertEqual(response.status_code, 201)

