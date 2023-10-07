FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code/

RUN mkdir src
RUN mkdir tests
COPY requirements.txt /code

WORKDIR /code
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src/ src/
COPY tests/ tests/

ENV PYTHONPATH=/code/src