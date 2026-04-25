from django.test import TestCase

from myapp.models import UserModel

class UserTestClass(TestCase):

    def test_user_creation(self):
        """Test POST request """
        response = self.client.post('/myapp/create-user/',
            data={
                "username": "mahmoud-twm-2026",
                "email": "mahmodud-twm-2026@local.com",
                "password": "1236549"
            }, 
            format='json',
            content_type='application/json'  # Explicitly set
        )

         # Check status code
        self.assertEqual(response.status_code, 201)


    def test_user_get_password(self):
        print("Hi")
        user = UserModel(username="myuser",password="mypassword123",email="mahmodud-twm-2026@local.com")
        print("Hi 2")

        user.save()

        print("Hi 3")

        user_info = UserModel.objects.get(id=user.id)

        print("Encrypted in DB:", user_info.password)
        print("Decrypted plain:", user_info.get_password())


