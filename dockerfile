FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install flask

ENV SERVER_ID=1

CMD ["python", "server.py"]