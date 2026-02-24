import grpc
import json

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from .proto_generated import service_pb2_grpc, service_pb2


def call_grpc(request):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        request_message = service_pb2.MessageRequest(name="John Doe")
        response = stub.GetMessage(request_message)

    return JsonResponse({'message': response.message})


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print("Received data:", data)
        
        # Validate required fields
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return JsonResponse({
                'success': False, 
                'message': 'Missing required fields'
            }, status=400)
        

        print("I am here")

        with grpc.insecure_channel('localhost:50051') as channel:
            print("gRPC recieve")

            stub = service_pb2_grpc.MyServiceStub(channel)
            # Example user data
            user_request = service_pb2.CreateUserRequest(
                username=username,
                email=email,
                password=password

            )
            grpc_response = stub.CreateUser(user_request, timeout=10)
            print("gRPC recieve", grpc_response)


        print("I am here 2")

        print("gRPC recieve", grpc_response)
        return JsonResponse({
            'success': grpc_response.success, 
            'message': grpc_response.message
        }, status=201 if grpc_response.success else 400)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    except grpc.RpcError as e:
        return JsonResponse({
            'success': False, 
            'message': f'gRPC error: {e.details()}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Server error: {str(e)}'
        }, status=500)


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
