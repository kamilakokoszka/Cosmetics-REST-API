FROM python:3.10-alpine3.18

ENV PYTHONUNBUFFERED 1

RUN mkdir /cosmetics_api
WORKDIR /cosmetics_api/

COPY requirements.txt /cosmetics_api/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /cosmetics_api/

EXPOSE 8000