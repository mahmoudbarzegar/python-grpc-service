from django.test import TestCase


class GRPCTestClass(TestCase):
    def test_call_grpc(self):
        """Test GET request to call_grpc endpoint."""
        response = self.client.get("/myapp/call-grpc/")

        # Check status code
        self.assertEqual(response.status_code, 200)
