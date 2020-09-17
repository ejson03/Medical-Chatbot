FROM python:3.7-slim as python_builder
RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  curl

COPY requirements.txt /app/requirements.txt
RUN apt-get update -qq && apt-get -y install build-essential  libffi-dev --fix-missing \
  && apt-get clean \
  && python3 -m pip install --upgrade pip wheel \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
  && pip3 install -r  /app/requirements.txt \
  && python3 -m spacy download en_core_web_md

# install poetry
# keep this in sync with the version in pyproject.toml and Dockerfile
ENV POETRY_VERSION 1.0.3
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# install dependencies
COPY . /app/
RUN python -m venv /opt/venv && \
  . /opt/venv/bin/activate && \
  pip install --no-cache-dir -U pip && \
  cd /app && \
  poetry install --no-dev --no-interaction

# start a new build stage
FROM python:3.7-slim

# copy everything from /opt
COPY --from=python_builder /opt/venv /opt/venv
COPY --from=python_builder /app /app
ENV PATH="/opt/venv/bin:$PATH"

# update permissions & change user
RUN chgrp -R 0 /app && chmod -R g=u /app
USER 1001

# change shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# create a mount point for custom actions and the entry point
WORKDIR /app
EXPOSE 5055
ENTRYPOINT ["./entrypoint.sh"]
CMD ["start", "--actions", "actions.actions"]
