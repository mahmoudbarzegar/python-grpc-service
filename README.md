# Sample gRPC Service with Python and Django

This repository provides a basic implementation of a gRPC service using Python and Django. It demonstrates how to set up a gRPC server and integrate it with Django for building scalable and efficient communication between client and server applications.

## Features

- **gRPC Server Setup**: Step-by-step configuration of a gRPC server with Django.
- **Protocol Buffers**: Includes `.proto` files for defining service contracts.
- **Django Integration**: Leverages Django’s ORM and features within the gRPC context.
- **Client-Server Communication**: Demonstrates seamless communication via gRPC.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Django (version 4.0 or higher recommended)
- gRPC tools for Python

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Compile Protocol Buffers**:

   ```bash
   python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/service.proto
   ```

5. **Run Migrations** (if using Django ORM):

   ```bash
   python manage.py migrate
   ```

6. **Start the gRPC Server**:
   ```bash
   python manage.py run_grpc_server
   ```

## Usage

1. **Define Services in `.proto` Files**:

   - Modify the `service.proto` file located in the `protos/` directory to define your gRPC services and messages.

2. **Implement Services**:

   - Add your gRPC service implementations in `grpc_services.py`.

3. **Run the Server**:

   - Start the gRPC server as shown in the installation steps.

4. **Test the Service**:
   - Use tools like [BloomRPC](https://github.com/bloomrpc/bloomrpc) or create a gRPC client script to test the service.

---

## Example Client Code

Below is an example of a Python client communicating with the gRPC server:

```python
import grpc
from django.http import JsonResponse

from .proto_generated import service_pb2_grpc,service_pb2


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

```

---

## Folder Structure

```
├── manage.py
├── grpc_service
├── myapp/
│   ├── grpc_services.py  # gRPC service implementations
│   ├── models.py         # Django models
│   ├── ...
├── protos/
│   ├── service.proto     # Protocol Buffers definitions
├── requirements.txt      # Dependencies
└── README.md
```

---

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements or report bugs.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Resources

- [gRPC Documentation](https://grpc.io/docs/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)

---

Happy Coding! 🚀
