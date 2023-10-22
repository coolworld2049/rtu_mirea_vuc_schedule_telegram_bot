#!/usr/bin/env bash

read -p "Enter revision message: " revision_message

alembic upgrade head &> /dev/null
alembic revision --autogenerate -m "${revision_message}"
alembic upgrade head
git add alembic