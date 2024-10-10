FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask

EXPOSE 9090

CMD ["python", "fibonacci_server.py"]