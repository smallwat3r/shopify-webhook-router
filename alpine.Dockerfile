FROM python:3.9-alpine3.13

RUN apk update \
  && apk add --no-cache \
    libffi-dev \
    musl-dev \
  && python -m pip install --upgrade pip

WORKDIR /opt/router

ENV GROUP=app
ENV USER=router
ENV UID=12345
ENV GID=23456

RUN mkdir -p /var/run/celery/
RUN addgroup --gid "$GID" "$GROUP" \
  && adduser --uid "$UID" \
    --disabled-password \
    --gecos "" \
    --ingroup "$GROUP" \
    "$USER"  \
  && chown "$USER:$GROUP" /var/run/celery/

USER "$USER"
ENV PATH="/home/$USER/.local/bin:${PATH}"

COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --no-warn-script-location \
    --user \
    -r requirements.txt \
  && find "/home/$USER/.local" \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' +

COPY --chown=$USER:$GROUP . .
