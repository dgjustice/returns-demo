FROM python:3.9

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

CMD ["python"]
