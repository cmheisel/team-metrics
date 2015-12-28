FROM debian:jessie

RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-dev \
    python3-venv \
    python3-pip \
    libpq-dev \
    && pip3 install -U pip \
    && rm -rf /var/lib/apt/lists/*

RUN pyvenv-3.4 /app-ve && mkdir -p /app/
COPY ./container/* /

WORKDIR /app/
COPY ./requirements*.txt /app/
RUN /app-ve/bin/pip install -r requirements.txt
COPY ./ /app

EXPOSE 8000

CMD ["/bin/sh", "/opt/entrypoint.sh"]
