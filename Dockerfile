FROM python:3.10-alpine3.18

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --no-cache postgresql-dev gcc musl-dev

RUN mkdir /cosmetics_api
WORKDIR /cosmetics_api/

COPY requirements.txt /cosmetics_api/
RUN pip install --upgrade pip \
    && pip install psycopg2-binary \
    && pip install --no-cache-dir -r requirements.txt

COPY . /cosmetics_api/

EXPOSE 8000