ARG build_env

FROM python:slim AS base
SHELL ["/bin/bash", "-c"]
WORKDIR /project
COPY Pipfile scripts ./
RUN ./pipenv_install.sh

FROM base AS development
COPY . .
CMD pipenv run flask db_fill && pipenv run flask run --host=0.0.0.0

#FROM base AS production
#COPY blog_application blog_application
