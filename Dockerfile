FROM python:3.11.6-slim-bullseye as build

RUN pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

WORKDIR /app

RUN poetry install

COPY . /app/

RUN poetry install


FROM build as migration

WORKDIR /app/telegram_bot

CMD ["python", "-m", "alembic", "upgrade", "head"]


FROM migration as prod

WORKDIR /app

CMD ["python", "-m", "telegram_bot"]