FROM python:slim AS base
SHELL ["/bin/bash", "-c"]
WORKDIR /project
COPY Pipfile scripts ./
ARG build_env
RUN ./pipenv_install.sh

FROM base AS development
COPY . .
CMD pipenv run flask db_fill && pipenv run devserver

FROM base AS production
COPY blog_app blog_app
COPY config.py .
CMD ./deploy.sh
