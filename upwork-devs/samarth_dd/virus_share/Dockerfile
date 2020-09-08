FROM python:3-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .
EXPOSE 80
CMD [ "python", "src" ]
