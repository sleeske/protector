ARG PYTHON_VERSION=3.9.5-buster

FROM python:3.9.5-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=True \
    PYTHON_ROOT=/pyroot \
    APP_DIR=/project/app

ENV PYTHONUSERBASE=$PYTHON_ROOT \
    PATH=$PYTHON_ROOT/bin:$PATH \
    PYTHONPATH=$PYTHONPATH:$APP_DIR/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gettext \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements/* ./
RUN pip install --user --no-cache-dir -r requirements-dev.txt

RUN addgroup --system --gid 102 django \
    && useradd -m -g django django \
    && mkdir -p $PYTHON_ROOT /project/static /project/media


WORKDIR $APP_DIR

COPY . $APP_DIR

RUN chown -R django: /project

USER django
