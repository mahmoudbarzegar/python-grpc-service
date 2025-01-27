import os
import sys

# Add the proto_generated directory to Python path
proto_generated_dir = os.path.join(os.path.dirname(__file__), 'proto_generated')
sys.path.append(proto_generated_dir)