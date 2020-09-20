FROM python:3.6
EXPOSE 50051
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
#CMD [ "python", "main.py" ]
CMD [ "python", "grpc_server.py" ]
