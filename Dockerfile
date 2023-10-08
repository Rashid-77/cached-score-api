FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
COPY requirements.txt /code

WORKDIR /code
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN mkdir src
COPY src/ src/

WORKDIR /code/
RUN mkdir tests
COPY tests/ tests/

ENV PYTHONPATH=/code/src