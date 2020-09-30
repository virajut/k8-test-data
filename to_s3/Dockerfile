FROM python:3.6
WORKDIR /usr/src/app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]
