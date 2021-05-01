# `base` sets all enviromental variables
FROM python:3.8-slim as python_base

# python variables
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python_base as install_base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps to install poetry
    curl \
    # deps for building python deps
    build-essential

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# copy project python dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev
RUN poetry add uwsgi

FROM install_base as production_base
COPY --from=install_base $PYSETUP_PATH $PYSETUP_PATH
COPY app app
COPY core core

COPY docker/run_app.sh /run_app.sh
RUN chmod +x /run_app.sh
RUN sed -i 's/\r$//' /run_app.sh

ENV DATABASE_PATH=sqlite:////database/database.db
