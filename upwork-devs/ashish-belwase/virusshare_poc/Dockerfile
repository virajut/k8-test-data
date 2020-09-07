FROM python:3.6
EXPOSE 5000
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "main.py" ]