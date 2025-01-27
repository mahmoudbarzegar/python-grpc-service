from django.core.management.base import BaseCommand
import subprocess
import sys
import os


class Command(BaseCommand):
    help = 'Run the gRPC server'

    def handle(self, *args, **kwargs):
        # grpc_server_path = os.path.join(os.path.dirname(__file__), '../../../grpc_server.py')
        # grpc_server_path = os.path.abspath(grpc_server_path)
        try:
            subprocess.run([sys.executable, 'myapp/grpc_server.py'], check=True)
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error starting gRPC server: {e}")
