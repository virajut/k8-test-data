FROM python:3.6
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 50052
CMD [ "python", "main.py" ]
