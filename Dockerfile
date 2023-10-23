FROM python:3.11.6-slim-bullseye

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install poetry==1.3.2

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install -n

COPY . /app/

WORKDIR /app/telegram_bot

CMD ["python", "-m", "alembic", "upgrade", "head"]

WORKDIR /app

CMD ["python", "-m", "telegram_bot"]
