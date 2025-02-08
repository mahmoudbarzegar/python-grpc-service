import grpc
import json

from django.http import JsonResponse

from .proto_generated import service_pb2_grpc, service_pb2


def call_grpc(request):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        request_message = service_pb2.MessageRequest(name="John Doe")
        response = stub.GetMessage(request_message)

    return JsonResponse({'message': response.message})


def create_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = service_pb2_grpc.MyServiceStub(channel)
            # Example user data
            user_request = service_pb2.CreateUserRequest(
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password')

            )
            response = stub.CreateUser(user_request, timeout=105)

        return JsonResponse({'success': response.success, 'message': response.message})

    except grpc.RpcError as e:
        # Handle gRPC errors properly
        return handle_grpc_error(e)


def handle_grpc_error(error):
    """Handles gRPC errors and returns a user-friendly JSON response."""

    status_code = error.code()
    details = error.details()

    error_messages = {
        grpc.StatusCode.UNAVAILABLE: "Service is unavailable. Please try again later.",
        grpc.StatusCode.DEADLINE_EXCEEDED: "Request timed out. Please try again.",
        grpc.StatusCode.INVALID_ARGUMENT: "Invalid input provided.",
        grpc.StatusCode.NOT_FOUND: "Requested resource was not found.",
        grpc.StatusCode.ALREADY_EXISTS: "Resource already exists.",
        grpc.StatusCode.PERMISSION_DENIED: "You do not have permission to perform this action.",
        grpc.StatusCode.UNAUTHENTICATED: "Authentication failed. Please log in again.",
        grpc.StatusCode.RESOURCE_EXHAUSTED: "Too many requests. Please slow down.",
        grpc.StatusCode.INTERNAL: "An internal server error occurred. Please try again later.",
        grpc.StatusCode.UNKNOWN: "An unknown error occurred.",
    }

    # Get user-friendly error message or fallback to default
    user_message = error_messages.get(status_code, "Something went wrong. Please try again.")

    return JsonResponse({"success": False, "error": user_message, "details": details}, status=500)
