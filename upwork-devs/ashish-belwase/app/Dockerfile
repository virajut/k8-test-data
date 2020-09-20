FROM python:3.6
EXPOSE 5000
ARG STATIC_PATH=/usr/src/app/src/static
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]
