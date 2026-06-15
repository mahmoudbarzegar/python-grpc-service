# app/tests/test_external_credential.py

from django.test import TestCase
from myapp.models import ExternalCredentialModel


class ExternalCredentialTests(TestCase):

    def test_password_encryption(self):
        cred = ExternalCredentialModel(
            service_name="smtp",
            username="admin@example.com",
        )

        cred.set_password("supersecret123")
        cred.save()

        obj = ExternalCredentialModel.objects.get(id=cred.id) # type: ignore

        self.assertNotEqual(obj.encrypted_password, "supersecret123") 
        self.assertEqual(obj.get_password(), "supersecret123")