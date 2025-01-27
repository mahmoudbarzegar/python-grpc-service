import grpc
from django.http import JsonResponse

from .proto_generated import service_pb2_grpc,service_pb2


def call_grpc(request):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub =  service_pb2_grpc.MyServiceStub(channel)
        request_message = service_pb2.MessageRequest(name="John Doe")
        response = stub.GetMessage(request_message)
    
    return JsonResponse({'message': response.message})

def create_user(request):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        # Example user data
        user_request = service_pb2.CreateUserRequest(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        response = stub.CreateUser(user_request)
    
    return JsonResponse({'success': response.success, 'message': response.message})
