FROM public.ecr.aws/docker/library/python:3.12.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/app/.venv/bin:$PATH"


RUN addgroup --gid 1000 app &&\
    adduser --home /app --uid 1000 --gid 1000 app

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y apt-utils \
    gcc \
    musl-dev \
    libpq-dev \
    curl


RUN python3 -m pip install --no-cache-dir --no-warn-script-location poetry

COPY poetry.lock pyproject.toml ./

RUN python3 -m poetry config virtualenvs.in-project true &&\
    python3 -m poetry install --no-cache --no-root

COPY . .

RUN chown -R app:app /app

USER app

ENTRYPOINT [ "python3" ]
CMD [ "-m", "gunicorn", "-b", "0.0.0.0:8000", "--workers", "1", "--access-logfile", "-",  "main:create_app", "--reload", "-k", "uvicorn.workers.UvicornWorker" ]
