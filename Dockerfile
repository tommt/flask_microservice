FROM python:3.9
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y curl

CMD /bin/bash

# Install poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN mkdir /app
RUN mkdir /app/staticfiles
RUN mkdir /app/mediafiles

WORKDIR /app
COPY . /app
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi