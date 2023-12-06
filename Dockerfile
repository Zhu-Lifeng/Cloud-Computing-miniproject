FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
COPY ssl_cert.crt /
COPY ssl_private.key /

EXPOSE 8080

CMD ["python", "main.py"]



