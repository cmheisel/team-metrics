FROM tatsushid/tinycore-python:2.7

RUN virtualenv /app-ve
RUN mkdir -p /app/
COPY ./container/* /

WORKDIR /app/
COPY ./requirements*.txt /app/
RUN /app-ve/bin/pip install -r requirements.txt
COPY ./team_metrics /app/

EXPOSE 8000

CMD ["/bin/sh", "/opt/entrypoint.sh"]
