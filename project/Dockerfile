# pull official base image
FROM python:3.9.6-slim-buster 

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# install system dependencies
RUN apt-get update \
  && apt-get -y install curl netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]