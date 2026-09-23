# ---------- Фронтенд: собираем Tailwind CSS ----------
FROM node:22-alpine AS frontend

WORKDIR /build/static
COPY static/package.json static/package-lock.json ./
RUN npm ci

# Tailwind ищет классы в шаблонах и python-коде
COPY templates /build/templates
COPY apps /build/apps
COPY static/src ./src
COPY static/scripts ./scripts
COPY static/icons.txt ./icons.txt
RUN npm run build

# ---------- Django ----------
FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install poetry

COPY poetry.lock pyproject.toml /var/www/project/

WORKDIR /var/www/project

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /var/www/project
COPY --from=frontend /build/static/dist /var/www/project/static/dist
COPY --from=frontend /build/templates/icons /var/www/project/templates/icons

EXPOSE 8000
