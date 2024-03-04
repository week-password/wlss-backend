FROM python:3.11-slim

WORKDIR /wlss-backend

RUN apt-get update \
    # we need 'enchant-2' for pylint's spellchecker
    && apt-get -y install enchant-2 \
    && pip install --upgrade pip \
    && pip install poetry==1.4.2

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

# api directory should be copied before poetry installation
# in that case poetry will be able to install this library
COPY api ./api
# we also need to install 'test' dependencies here, because linters check tests code as well
# otherwise linters will report 'module not found' errors for tests code
RUN poetry install --with=app,lint,test

COPY . ./
