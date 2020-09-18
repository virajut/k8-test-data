import grpc
from concurrent import futures
import time

from src.rpc.file_pb2 import Response
from src.rpc.file_pb2_grpc import FileServicer, add_FileServicer_to_server
from src.rpc.file import get_file


class FileServicer(FileServicer):
    def MaliciousFile(self, request, context):
        response = Response()
        response.data = get_file(type=request.type, num_files=request.num_files)
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

add_FileServicer_to_server(FileServicer(), server)

# listen on port 50051
print("Starting server. Listening on port 50051.")
server.add_insecure_port("[::]:50051")
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
