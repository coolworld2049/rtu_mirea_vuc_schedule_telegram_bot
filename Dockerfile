FROM python:3.11.6-slim-bullseye

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install poetry==1.3.2

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install

COPY . /app/

RUN poetry install

WORKDIR /app/telegram_bot

CMD ["python", "-m", "alembic", "upgrade", "head"]

WORKDIR /app

CMD ["python", "-m", "telegram_bot"]
