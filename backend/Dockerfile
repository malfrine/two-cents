FROM python:3.8

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH="${PYTHONPATH}:/app/core/apps/pennies:/app/core"

# python dependencies
COPY ./requirements.txt /
RUN pip install -r ./requirements.txt

USER root
RUN apt-get update
RUN apt-get install -y coinor-cbc


# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/start.sh ./scripts/gunicorn.sh /

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh && sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh &&\
    sed -i 's/\r$//g' /gunicorn.sh && chmod +x /gunicorn.sh

WORKDIR /app
