import grpc
import time
import os
import sys

from concurrent import futures

proto_generated_dir = os.path.join(os.path.dirname(__file__), 'proto_generated')
sys.path.append(proto_generated_dir)

import proto_generated.service_pb2_grpc as service_pb2_grpc
import proto_generated.service_pb2 as service_pb2

class MyServiceServicer(service_pb2_grpc.MyServiceServicer):
    def GetMessage(self, request, context):
        response = service_pb2.MessageResponse()
        response.message = f"Hello, {request.name}!"
        return response
    
    def CreateUser(self, request, context):
        # Example logic for user creation
        if not request.username or not request.email or not request.password:
            return service_pb2.CreateUserResponse(success=False, message="Invalid input")
    
        # Simulate user creation (replace with actual database logic)
        print(f"Creating user: {request.username}, {request.email}")
        return service_pb2.CreateUserResponse(success=True, message="User created successfully!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    # user_pb2_grpc.add_UserServiceServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051...")
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
