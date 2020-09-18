import grpc

from src.rpc.file_pb2 import Input
from src.rpc.file_pb2_grpc import FileStub

options = [("grpc.max_receive_message_length", 500 * 1024 * 1024)]
channel = grpc.insecure_channel("localhost:50051", options=options)

stub = FileStub(channel)

_input = Input(type="pdf", num_files=1)

response = stub.MaliciousFile(_input)
with open("malicious.zip", "wb") as fp:
    fp.write(response.data)
